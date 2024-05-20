from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import serial
import json
import cv2
import os
from datetime import datetime
from threading import Thread

from icecream import ic

app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "weights.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class WeightData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight_before = db.Column(db.Float, nullable=False)
    weight_after = db.Column(db.Float, nullable=True)
    image_path = db.Column(db.String(255), nullable=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    def __repr__(self):
        if self.weight_before and self.weight_after:
            return f"<{self.id} | WeightData {self.weight_after - self.weight_before} >"
        return f"<{self.id} | WeightData {self.weight_before} >"


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("weight.html", title="WeighPy")


@app.route("/weights")
def show_weights():
    weights = WeightData.query.order_by(WeightData.created_at.desc()).all()
    ic(weights)
    return render_template("weight.html", weights=weights)


@app.route("/weights/<int:weight_id>/update", methods=["GET", "POST"])
def update_weight(weight_id):
    weight = WeightData.query.get_or_404(weight_id)
    if request.method == "POST":
        weight.weight_before = request.form["weight_before"]
        weight.weight_after = request.form["weight_after"]
        db.session.commit()
        return redirect(url_for("show_weights"))
    return render_template("update_weight.html", title="Update Weight", weight=weight)


@app.route("/weights/<int:weight_id>/delete", methods=["POST"])
def delete_weight(weight_id):
    weight = WeightData.query.get_or_404(weight_id)
    db.session.delete(weight)
    db.session.commit()
    return redirect(url_for("show_weights"))


def capture_image():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        image_dir = os.path.join(basedir, "static/images")
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(image_dir, f"{timestamp}.jpg")
        cv2.imwrite(image_path, frame)
        cam.release()
        return image_path
    cam.release()
    return None


def process_arduino_data():
    ser = serial.Serial("/dev/ttyUSB0", 9600)
    total_weight = 0.0
    num_readings = 0
    has_vehicle = False

    with app.app_context():
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode("utf-8").strip()
                json_data = json.loads(data)

                ic(json_data)
                current_has_vehicle = bool(json_data.get("hasVehicle"))
                ic(current_has_vehicle)
                weight = json_data.get("weight")
                ic(weight)

                if current_has_vehicle:
                    total_weight += weight
                    num_readings += 1
                    if not has_vehicle:
                        #     image_path = capture_image()
                        weight_before = weight
                else:
                    if has_vehicle:
                        if num_readings > 0:
                            average_weight = total_weight / num_readings
                            ic(average_weight)
                            new_entry = WeightData(
                                weight_before=weight_before,
                                weight_after=average_weight,
                                # image_path=image_path,
                            )
                            db.session.add(new_entry)
                            db.session.commit()
                        total_weight = 0.0
                        num_readings = 0
                        image_path = None

                has_vehicle = current_has_vehicle


arduino_thread = Thread(target=process_arduino_data)
arduino_thread.daemon = True
arduino_thread.start()

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)

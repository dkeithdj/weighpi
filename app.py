from flask import Flask

# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weight.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#
# db = SQLAlchemy(app)


# class WeightData(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     weight_before = db.Column(db.Float, nullable=False)
#     weight_after = db.Column(db.Float, nullable=True)
#     created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
#     updated_at = db.Column(
#         db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now()
#     )
#
#     def __repr__(self):
#         if self.weight_before and self.weight_after:
#             return f"<{self.id} | WeightData {self.weight_after - self.weight_before} >"
#         return f"<{self.id} | WeightData {self.weight_before} >"


@app.route("/")
def index():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

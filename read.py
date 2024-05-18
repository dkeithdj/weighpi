import serial
import json


def main():

    ser = serial.Serial(
        "/dev/ttyUSB0", 9600
    )  # Change ACM0 to the port your Arduino is connected to

    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode("utf-8").strip()
            json_data = json.loads(data)
            print(json_data["sensor_front"])
            print(json_data["sensor_rear"])
            print(json_data["weight"])
            print(json_data["hasVehicle"])

            # if data.startswith("W,"):
            #     weight_data = float(data.split(",")[1])
            #     print("Average Weight:", weight_data)


if __name__ == "__main__":
    main()

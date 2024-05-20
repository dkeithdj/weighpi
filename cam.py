import cv2
import os
from datetime import datetime


def capture_image():
    # Open the default camera
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Error: Could not open camera.")
        return None

    # Read a frame from the camera
    ret, frame = cam.read()

    if not ret:
        print("Error: Could not read frame.")
        cam.release()
        return None

    # Create a directory to save images if it doesn't exist
    image_dir = os.path.join(os.getcwd(), "images")
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    # Generate a unique filename based on the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = os.path.join(image_dir, f"{timestamp}.jpg")

    # Save the captured frame as an image file
    cv2.imwrite(image_path, frame)

    # Release the camera
    cam.release()

    print(f"Image saved at {image_path}")
    return image_path


if __name__ == "__main__":
    capture_image()

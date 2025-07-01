import cv2
import time
from picamera2 import Picamera2

# Initialize Pi camera
picam2 = Picamera2()

# Configure for preview with RGB output
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
picam2.configure(config)
picam2.start()

# Let the camera warm up
time.sleep(1)

print("[INFO] Press 'q' to exit.")

try:
    while True:
        # Capture image as numpy array
        frame = picam2.capture_array()

        # Optional: Draw a static box
        cv2.rectangle(frame, (150, 100), (450, 400), (0, 255, 0), 2)

        # Display the image
        cv2.imshow("Pi Camera Feed", frame)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] Quitting.")
            break

except KeyboardInterrupt:
    print("\n[INFO] Interrupted by user.")

finally:
    picam2.stop()
    cv2.destroyAllWindows()
    print("[INFO] Camera stopped, windows closed.")


"""

Install the required libraries
- sudo apt update
- sudo apt install -y python3-picamera2 libcamera-dev
Benefits:
- Works natively with Pi Camera v1/v2/HQ/v3

- Uses libcamera, which is the official Pi camera framework on Pi OS Bullseye and Bookworm

- Full resolution, format, and stream control

- Modern and future-proof (OpenCV is no longer maintained for Pi camera modules)


"""
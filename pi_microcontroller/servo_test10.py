import pigpio
import time

# Setup pigpio
pi = pigpio.pi()

if not pi.connected:
    print("Failed to connect to pigpio daemon!")
    exit()

# Define your Servo class
class Servo:
    def __init__(self, pin):
        self.pin = pin
        pi.set_mode(pin, pigpio.OUTPUT)
        self.current_angle = 0

    def angle_to_pulse(self, angle):
        # Convert angle to pulse width (1000 - 2000 µs for 0° - 180°)
        return 1000 + (angle * 1000 / 180)

    def write(self, angle):
        pulsewidth = self.angle_to_pulse(angle)
        pi.set_servo_pulsewidth(self.pin, pulsewidth)
        self.current_angle = angle
        time.sleep(0.02)

    def read(self):
        return self.current_angle

    def stop(self):
        pi.set_servo_pulsewidth(self.pin, 0)  # Stops the servo

# Assign GPIO pins for each finger
# Adjust pin numbers based on your actual wiring
leftHandPins = {
    "thumb": 9,
    "index": 12,
    "middle": 11,
    "ring": 6,
    "pinky": 5
}

rightHandPins = {
    "thumb": 13,
    "index": 16,
    "middle": 19,
    "ring": 20,
    "pinky": 21
}

# Create servo instances for both hands
leftHandServos = {finger: Servo(pin) for finger, pin in leftHandPins.items()}
rightHandServos = {finger: Servo(pin) for finger, pin in rightHandPins.items()}

# Constants
smoothDelay = 0.01
OPEN = 0
CLOSED = 180
HALF_CLOSED = 90
RELAXED = 45

# Smooth movement function
def smooth_move(servo, target, delay_time):
    current = servo.read()
    if current < target:
        for pos in range(current, target + 1, 4):
            servo.write(pos)
            time.sleep(delay_time)
    else:
        for pos in range(current, target - 1, -5):
            servo.write(pos)
            time.sleep(delay_time)

# Combined hand actions
def openAllFingers():
    print("Opening all fingers")
    for servo in list(leftHandServos.values()) + list(rightHandServos.values()):
        smooth_move(servo, OPEN, smoothDelay)

def closeAllFingers():
    print("Closing all fingers")
    for servo in list(leftHandServos.values()) + list(rightHandServos.values()):
        smooth_move(servo, CLOSED, smoothDelay)

# Add more gestures as needed...

try:
    while True:
        openAllFingers()
        time.sleep(2)
        closeAllFingers()
        time.sleep(2)

except KeyboardInterrupt:
    print("Exiting gracefully...")
    for servo in list(leftHandServos.values()) + list(rightHandServos.values()):
        servo.stop()
    pi.stop()

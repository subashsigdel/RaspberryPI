import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)  # or GPIO.BOARD depending on your wiring

# Define your Servo class
class Servo:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, 50)  # 50Hz frequency
        self.pwm.start(0)
        self.current_angle = 0

    def angle_to_duty(self, angle):
        return 2 + (angle / 18)

    def write(self, angle):
        duty = self.angle_to_duty(angle)
        self.pwm.ChangeDutyCycle(duty)
        self.current_angle = angle
        time.sleep(0.02)

    def read(self):
        return self.current_angle

    def stop(self):
        self.pwm.stop()

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
    GPIO.cleanup()

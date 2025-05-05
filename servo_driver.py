import time
import smbus2
from adafruit_pca9685 import PCA9685

# Set up I2C bus and PCA9685 (using smbus2)
i2c = smbus2.SMBus(1)  # 1 is the I2C bus on Raspberry Pi
pca = PCA9685(i2c)
pca.frequency = 50  # Servo control frequency

# Convert angle to duty cycle
def angle_to_pwm(angle):
    pulse = 500 + (angle / 180.0) * 2000  # microseconds
    duty = int((pulse / 20000.0) * 0xFFFF)
    return duty

class Servo:
    def __init__(self, channel):
        self.channel = channel
        self.angle = 0

    def write(self, angle):
        pwm = angle_to_pwm(angle)
        pca.channels[self.channel].duty_cycle = pwm
        self.angle = angle
        time.sleep(0.02)

    def read(self):
        return self.angle

# Assign servos to fingers (using channels 0 to 4)
thumb = Servo(0)
index = Servo(1)
middle = Servo(2)
ring = Servo(3)
pinky = Servo(4)

# Constants for gestures
OPEN = 0
CLOSED = 180
RELAXED = 45
DELAY = 0.01

# Smooth move function
def smooth_move(servo, target):
    current = servo.read()
    step = 4 if target > current else -4
    for angle in range(current, target + step, step):
        servo.write(angle)
        time.sleep(DELAY)

# Hand gestures
def open_hand():
    print("Opening hand")
    for servo in [thumb, index, middle, ring, pinky]:
        smooth_move(servo, OPEN)

def close_hand():
    print("Closing hand")
    for servo in [thumb, index, middle, ring, pinky]:
        smooth_move(servo, CLOSED)

def thumbs_up():
    print("Thumbs up!")
    smooth_move(thumb, OPEN)
    for servo in [index, middle, ring, pinky]:
        smooth_move(servo, CLOSED)

def peace_sign():
    print("Peace sign")
    smooth_move(index, OPEN)
    smooth_move(middle, OPEN)
    for servo in [thumb, ring, pinky]:
        smooth_move(servo, CLOSED)

# Main loop
try:
    while True:
        open_hand()
        time.sleep(1)
        close_hand()
        time.sleep(1)
        thumbs_up()
        time.sleep(1)
        peace_sign()
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
    pca.deinit()


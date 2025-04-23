import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)  # or GPIO.BOARD depending on your pin setup

# Define your Servo class
class Servo:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, 50)  # 50Hz frequency
        self.pwm.start(0)
        self.current_angle = 0  # manually track the angle

    def angle_to_duty(self, angle):
        return 2 + (angle / 18)

    def write(self, angle):
        duty = self.angle_to_duty(angle)
        self.pwm.ChangeDutyCycle(duty)
        self.current_angle = angle
        time.sleep(0.02)  # Small delay to allow servo to move

    def read(self):
        return self.current_angle

    def stop(self):
        self.pwm.stop()

# Create servo instances
thumbServo = Servo(9)
indexServo = Servo(12)
middleServo = Servo(11)
ringServo = Servo(6)
pinkyServo = Servo(5)

# Movement speeds
smoothDelay = 0.01
fastDelay = 0.001

# Servo positions
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
        for pos in range(current, target - 1, -1):
            servo.write(pos)
            time.sleep(delay_time)

# Example gesture functions
def openAllFingers():
    print("Opening all fingers")
    smooth_move(thumbServo, OPEN, smoothDelay)
    smooth_move(indexServo, OPEN, smoothDelay)
    smooth_move(middleServo, OPEN, smoothDelay)
    smooth_move(ringServo, OPEN, smoothDelay)
    smooth_move(pinkyServo, OPEN, smoothDelay)

def closeAllFingers():
    print("Closing all fingers")
    smooth_move(thumbServo, CLOSED, smoothDelay)
    smooth_move(indexServo, CLOSED, smoothDelay)
    smooth_move(middleServo, CLOSED, smoothDelay)
    smooth_move(ringServo, CLOSED, smoothDelay)
    smooth_move(pinkyServo, CLOSED, smoothDelay)

# More functions like relaxedHand(), thumbsUp(), etc. (same logic)

try:
    while True:
        openAllFingers()
        time.sleep(2)
        closeAllFingers()
        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()


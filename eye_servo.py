from gpiozero import Servo
from time import sleep

# Replace with actual GPIO pins
horizontal_servo = Servo(17)  # GPIO17
vertical_servo = Servo(18)    # GPIO18

# Angle mapping helpers
def angle_to_pulse(value):
    # Maps 0–180 degrees to -1 to 1 range for gpiozero Servo
    return (value / 90.0) - 1

# Horizontal Eye Movement
def look_left():
    for angle in range(90, 44, -2):
        horizontal_servo.value = angle_to_pulse(angle)
        sleep(0.015)
    sleep(0.5)

def look_right():
    for angle in range(90, 136, 2):
        horizontal_servo.value = angle_to_pulse(angle)
        sleep(0.015)
    sleep(0.5)

def eye_center_from_left():
    for angle in range(45, 91, 2):
        horizontal_servo.value = angle_to_pulse(angle)
        sleep(0.015)
    sleep(0.5)

def eye_center_from_right():
    for angle in range(135, 89, -2):
        horizontal_servo.value = angle_to_pulse(angle)
        sleep(0.015)
    sleep(0.5)

# Vertical Eye Movement
def eye_up():
    for angle in range(90, 44, -2):
        vertical_servo.value = angle_to_pulse(angle)
        sleep(0.015)
    sleep(0.5)

def eye_down():
    for angle in range(90, 146, 2):
        vertical_servo.value = angle_to_pulse(angle)
        sleep(0.015)
    sleep(0.5)

def eye_center_from_up():
    for angle in range(45, 91, 2):
        vertical_servo.value = angle_to_pulse(angle)
        sleep(0.015)
    sleep(0.5)

def eye_center_from_down():
    for angle in range(145, 89, -2):
        vertical_servo.value = angle_to_pulse(angle)
        sleep(0.015)
    sleep(0.5)

from gpiozero import Servo
from time import sleep

# GPIO pins
neck_servo = Servo(22)  # GPIO22
jaw_servo = Servo(23)   # GPIO23

def angle_to_pulse(value):
    return (value / 90.0) - 1

# Neck movement
def neck_move_left():
    for angle in range(90, -1, -1):
        neck_servo.value = angle_to_pulse(angle)
        sleep(0.015)
    sleep(1)

def neck_center_from_left():
    for angle in range(0, 91):
        neck_servo.value = angle_to_pulse(angle)
        sleep(0.015)
    sleep(1)

def neck_move_right():
    for angle in range(90, 181):
        neck_servo.value = angle_to_pulse(angle)
        sleep(0.015)
    sleep(1)

def neck_center_from_right():
    for angle in range(180, 89, -1):
        neck_servo.value = angle_to_pulse(angle)
        sleep(0.015)
    sleep(1)

# Jaw movement
def jaw_open():
    for angle in range(90, 161, 10):
        jaw_servo.value = angle_to_pulse(angle)
        sleep(0.005)
    sleep(1)

def jaw_close():
    for angle in range(160, 89, -10):
        jaw_servo.value = angle_to_pulse(angle)
        sleep(0.005)
    sleep(1)

# Center everything
def center_all():
    neck_servo.value = angle_to_pulse(90)
    jaw_servo.value = angle_to_pulse(90)
    sleep(1)

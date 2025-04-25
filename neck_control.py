import pigpio
from time import sleep

pi = pigpio.pi()

NECK_PIN = 22
JAW_PIN = 23

def angle_to_pulse(angle):
    return int(500 + (angle * 2000 / 180))

def set_servo(pin, angle):
    pi.set_servo_pulsewidth(pin, angle_to_pulse(angle))

def neck_move_left():
    for angle in range(90, 0, -2):
        set_servo(NECK_PIN, angle)
        sleep(0.015)
    sleep(1)

def neck_center_from_left():
    for angle in range(0, 91, 2):
        set_servo(NECK_PIN, angle)
        sleep(0.015)
    sleep(1)

def neck_move_right():
    for angle in range(90, 181, 2):
        set_servo(NECK_PIN, angle)
        sleep(0.015)
    sleep(1)

def neck_center_from_right():
    for angle in range(180, 89, -2):
        set_servo(NECK_PIN, angle)
        sleep(0.015)
    sleep(1)

def jaw_open():
    for angle in range(90, 161, 10):
        set_servo(JAW_PIN, angle)
        sleep(0.005)
    sleep(1)

def jaw_close():
    for angle in range(160, 89, -10):
        set_servo(JAW_PIN, angle)
        sleep(0.005)
    sleep(1)

def center_all():
    set_servo(NECK_PIN, 90)
    set_servo(JAW_PIN, 90)
    set_servo(17, 90)  # Horizontal Eye
    set_servo(18, 90)  # Vertical Eye
    sleep(1)

import pigpio
from time import sleep

pi = pigpio.pi()

HORIZONTAL_PIN = 17
VERTICAL_PIN = 18

def angle_to_pulse(angle):
    return int(500 + (angle * 2000 / 180))  # 0–180° to 500–2500µs

def set_servo(pin, angle):
    pi.set_servo_pulsewidth(pin, angle_to_pulse(angle))

def look_left():
    for angle in range(90, 44, -2):
        set_servo(HORIZONTAL_PIN, angle)
        sleep(0.015)
    sleep(0.5)

def look_right():
    for angle in range(90, 136, 2):
        set_servo(HORIZONTAL_PIN, angle)
        sleep(0.015)
    sleep(0.5)

def eye_center_from_left():
    for angle in range(45, 91, 2):
        set_servo(HORIZONTAL_PIN, angle)
        sleep(0.015)
    sleep(0.5)

def eye_center_from_right():
    for angle in range(135, 89, -2):
        set_servo(HORIZONTAL_PIN, angle)
        sleep(0.015)
    sleep(0.5)

def eye_up():
    for angle in range(90, 44, -2):
        set_servo(VERTICAL_PIN, angle)
        sleep(0.015)
    sleep(0.5)

def eye_down():
    for angle in range(90, 146, 2):
        set_servo(VERTICAL_PIN, angle)
        sleep(0.015)
    sleep(0.5)

def eye_center_from_up():
    for angle in range(45, 91, 2):
        set_servo(VERTICAL_PIN, angle)
        sleep(0.015)
    sleep(0.5)

def eye_center_from_down():
    for angle in range(145, 89, -2):
        set_servo(VERTICAL_PIN, angle)
        sleep(0.015)
    sleep(0.5)

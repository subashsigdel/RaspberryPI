from eye_control import *
from neck_control import *
from time import sleep

def setup():
    center_all()

def loop():
    while True:
        # Neck movement
        neck_move_left()
        neck_center_from_left()
        sleep(0.5)

        neck_move_right()
        neck_center_from_right()
        sleep(0.5)

        # Jaw movement
        jaw_open()
        sleep(0.3)
        jaw_close()
        sleep(0.3)

        # Eye movement
        look_left()
        eye_center_from_left()
        sleep(0.5)

        look_right()
        eye_center_from_right()
        sleep(0.5)

        # Look up and down
        eye_up()
        eye_center_from_up()
        sleep(0.5)

        eye_down()
        eye_center_from_down()
        sleep(0.5)

if __name__ == "__main__":
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
        center_all()

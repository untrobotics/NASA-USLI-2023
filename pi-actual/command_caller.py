from aprs import functions
from aprs.functions import AprsFrame
#from picamera2 import Picamera2, Preview
import time

import datetime

#import camera_controller

from lib.servo.main import ContinuousServo
from lib.camera.main import Camera

# Yes I do like type hints, no I won't not use them
target_call_sign: str = 'KD9UDA'  # Sebastian King's call sign. Using it because we'll use it for testing later

servo = ContinuousServo(12, 23)
camera = Camera()

# Parses the information sent and calls the corresponding commands
def parse_frame_info(info: str):
    commands = info.split(' ')
    print("Commands:", commands)
    for cmd in commands:
        if cmd == 'A1': # right
             print("A1: rotate motor 60 degrees clockwise (right)")
             servo.rotate(ContinuousServo.ANTI_CLOCKWISE, 60)
        elif cmd == 'B2': # left
             print("B2: rotate motor 60 degress anti-clockwise (left)")
             servo.rotate(ContinuousServo.CLOCKWISE, 60)
        elif cmd == 'C3':
             print("C3: capture picture")
             camera.capture()
        elif cmd == 'D4':
             print("D4: to grayscale")
             camera.to_grayscale()
        elif cmd == 'E5':
             print("E5: to colour")
             camera.to_colour()
        elif cmd == 'F6':
             print("F6: rotate image")
             camera.rotate_image()
        elif cmd == 'G7':
             print("G7: apply a filter (invert)")
             camera.apply_sfx()
        elif cmd == 'H8':
             print("H8: remove all filters")
             camera.remove_all_filters()
        else:
            print(f'Invalid command! Command was {cmd}')


# Reads the frame received from the TCP socket and does stuff (to be decided)
def read_frame(frame):
    aprsFrame: AprsFrame = functions.parse_frame(frame)
    print(f'Entire frame was {aprsFrame}')  # Debugging print to see if the frame is a good frame

    # Make sure the source is from who we want it from (we don't want to parse APRS from someone besides NASA)
    if str(aprsFrame.source) == target_call_sign:
        # print(f'Info is {str(aprsFrame.info)[1:]}')
        parse_frame_info(str(aprsFrame.info)[1:])
    else:  # Output that it was wrong (also debugging)
        print(f'Not right source callsign. Callsign was {aprsFrame.source}')

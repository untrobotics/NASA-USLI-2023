from aprs import functions
from aprs.functions import AprsFrame
from picamera2 import Picamera2, Preview
import time

import datetime

#import camera_controller

from lib.servo.main import Servo

# Yes I do like type hints, no I won't not use them
target_call_sign: str = 'KD9UDA'  # Sebastian King's call sign. Using it because we'll use it for testing later

picam2 = Picamera2()
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)
picam2.start()

servo = Servo(12, 23)

# Parses the information sent and calls the corresponding commands
def parse_frame_info(info: str):
    commands = info.split(' ')
    print("Commands:", commands)
    for cmd in commands:
        if cmd == 'A1': # right
             print("rotate motor right")
             servo.rotate(Servo.ANTI_CLOCKWISE, 60)
        elif cmd == 'B2': # left
             print("rotate motor left")
             servo.rotate(Servo.CLOCKWISE, 60)
        elif cmd == 'C3':
             photo_filename = '/home/pi/capture/%s.jpg' % datetime.datetime.now()
             print("taking picture, will place it at:", photo_filename)
             picam2.capture_file(photo_filename)
        elif cmd == 'D4':
            camera_controller.to_grayscale()
        elif cmd == 'E5':
            camera_controller.to_color()
        elif cmd == 'F6':
            camera_controller.rotate_image()
        elif cmd == 'G7':
            camera_controller.apply_sfx()
        elif cmd == 'H8':
            camera_controller.remove_all_filters()
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

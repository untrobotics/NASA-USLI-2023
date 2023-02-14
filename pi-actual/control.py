#!/usr/bin/env python

from kiss import KISS

import kiss
import command_caller
from lib.landing_detection.main import LandingDetection

print("Hello")

landing_detection = LandingDetection()

def loop(ki: KISS):
    ki.start()
    print("Loop started");

    # get our info without DTI using str(functions.parse_frame_ax25(frame).info)[1:]
    ki.read(callback=command_caller.read_frame)


def main():
    try:
        print("Landing detection starting...")
        landing_detection.detect_landing()
        print("Phoenix has landed!")

        print("Beginning...")
        ki = kiss.TCPKISS(host='localhost', port=8001)
        print("Kissed")

        loop(ki)
    except KeyboardInterrupt:
        print("KBI")
        return
    except Exception as e:
        print("Error occurred in main loop, re-running...", e)
        main()

if __name__ == '__main__':
    print("Calling main")
    main()

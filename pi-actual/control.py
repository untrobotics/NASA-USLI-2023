#!/usr/bin/env python

from kiss import KISS

import kiss
import command_caller

print("Hello")

def loop(ki: KISS):
    ki.start()
    print("Loop started");

    # get our info without DTI using str(functions.parse_frame_ax25(frame).info)[1:]
    ki.read(callback=command_caller.read_frame)


def main():
    print("Beginning...")
    ki = kiss.TCPKISS(host='localhost', port=8001)
    print("Kissed")

    loop(ki)

if __name__ == '__main__':
    print("Calling main")
    main()

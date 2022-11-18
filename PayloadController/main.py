#!/usr/bin/env python

from kiss import KISS

import kiss
import command_caller


def loop(ki: KISS):
    ki.start()

    # get our info without DTI using str(functions.parse_frame_ax25(frame).info)[1:]
    ki.read(callback=command_caller.read_frame)


def main():
    ki = kiss.TCPKISS(host='localhost', port=8001)

    # I have no idea if this is good practice, but the running the script without payload_controller open throws an error (
    # because payload_controller hasn't opened the tcp port [duh]). It just looks dumb... probably don't need it if you aren't
    # testing with stdin on payload_controller
    while True:
        try:
            loop(ki)
        except:
            continue


if __name__ == '__main__':
    main()

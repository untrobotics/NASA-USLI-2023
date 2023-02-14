#!/usr/bin/env python
import sys
import traceback

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
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()

        # Extract unformatter stack traces as tuples
        trace_back = traceback.extract_tb(ex_traceback)

        # Format stacktrace
        stack_trace = list()

        for trace in trace_back:
            stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

        print("Exception type : %s " % ex_type.__name__)
        print("Exception message : %s" % ex_value)
        print("Stack trace : %s" % stack_trace)
        main()

if __name__ == '__main__':
    print("Calling main")
    main()

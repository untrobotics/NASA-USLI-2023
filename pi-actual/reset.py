#!/usr/bin/env python
import sys
import traceback

from lib.simple_servo.main import SimpleServo

from time import sleep

def main():
    try:
        print("Actuating the required servos...")
        door_servo_left = SimpleServo(19)
        door_servo_right = SimpleServo(26)
        parachute_release_servo = SimpleServo(13)

        door_servo_left.set_position(0)
        door_servo_right.set_position(0)
        parachute_release_servo.set_position(0)
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
        sleep(10)
        main()

if __name__ == '__main__':
    print("Calling main")
    main()

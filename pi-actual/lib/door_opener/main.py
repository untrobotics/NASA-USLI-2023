import time

import pigpio
import board
import adafruit_bno055
from ..simple_servo.main import SimpleServo
from time import sleep
from collections import deque

class DoorOpener:

    pitch_threshold = 1 # degrees
    def __init__(self, left_servo_gpio, right_servo_gpio, tilt_sensor_l_gpio, tilt_sensor_r_gpio):
        self.l_servo = SimpleServo(left_servo_gpio)
        self.r_servo = SimpleServo(right_servo_gpio)
        self.tilt_sensor_l_gpio = tilt_sensor_l_gpio
        self.tilt_sensor_r_gpio = tilt_sensor_r_gpio
        self.bno = adafruit_bno055.BNO055_I2C(board.I2C())
        self.pi = pigpio.pi()
        self.pi.set_mode(self.tilt_sensor_l_gpio, pigpio.INPUT)
        self.pi.set_mode(self.tilt_sensor_r_gpio, pigpio.INPUT)
        self.pi.set_mode(self.tilt_sensor_l_gpio, pigpio.PUD_DOWN)
        self.pi.set_mode(self.tilt_sensor_r_gpio, pigpio.PUD_DOWN)
        self.euler_readings = deque([-900 for i in range(10)])

#    def open_doors(self):
#        self.l_servo.set_position(50)
#        self.r_servo.set_position(50)
#        l_pos = 50
#        r_pos = 50
#        sleep(2)    # To allow time to get the things in position
#        print('Servos in required position...Adjusting for tilt')
#        condition = True
#        while condition:
#            condition = False
#            if not self.pi.read(self.tilt_sensor_l_gpio) and l_pos < 180:
#                condition = True
#                l_pos += 1
#                self.l_servo.set_position(l_pos)
#                print("Left servo position: %s degrees", l_pos)
#            if not self.pi.read(self.tilt_sensor_r_gpio) and r_pos < 180:
#                r_pos += 1
#                self.r_servo.set_position(r_pos)
#                condition = True
#                print("Right servo position: %s degrees", r_pos)
#        self.euler_readings = deque([0 for i in range(10)])

    def open_doors(self):
        l_pos = 50
        r_pos = 50
        self.l_servo.set_position(l_pos)
        time.sleep(5)
        self.r_servo.set_position(r_pos)

        sleep(2)    # To allow time to get the things in position
        print('Servos in required position...Adjusting for tilt')
        count = 0
        while True:
            time.sleep(0.1)
            if self.bno.euler[0] is None:
                self.bno.mode = adafruit_bno055.NDOF_MODE
                continue
            self.euler_readings.append(self.bno.euler[1])
            print("Euler val:", self.euler_readings[-1])
            self.euler_readings.popleft()
            if abs(max(self.euler_readings) - min(self.euler_readings)) < 3:
                if self.euler_readings[-1] > self.pitch_threshold:
                    if l_pos >= 180:
                        continue
                    l_pos += 1
                    self.l_servo.set_position(l_pos)
                    print("Left servo position: %s degrees", l_pos)
                    count = 0
                elif self.euler_readings[-1] < -self.pitch_threshold:
                    if r_pos >=180:
                        continue
                    r_pos += 1
                    self.r_servo.set_position(r_pos)
                    print("Right servo position: %s degrees", r_pos)
                    count = 0
                else:
                    count += 1
            elif abs(self.euler_readings[-1]-self.euler_readings[-2]) < 3:
                if self.euler_readings[-1] > self.pitch_threshold:
                    if l_pos >= 180:
                        continue
                    l_pos += 1
                    self.l_servo.set_position(l_pos)
                    print("Left servo position: %s degrees", l_pos)
                    count = 0
                elif self.euler_readings[-1] < -self.pitch_threshold:
                    if r_pos >= 180:
                        continue
                    r_pos += 1
                    self.r_servo.set_position(r_pos)
                    print("Right servo position: %s degrees", r_pos)
                    count = 0
                else:
                    count += 1
            if count >= 30:
                print('Done opening doors')
                break
            # condition = False
            # if not self.pi.read(self.tilt_sensor_l_gpio) and l_pos < 180:
            #     condition = True
            #     l_pos += 1
            #     self.l_servo.set_position(l_pos)
            #     print("Left servo position: %s degrees", l_pos)
            # if not self.pi.read(self.tilt_sensor_r_gpio) and r_pos < 180:
            #     r_pos += 1
            #     self.r_servo.set_position(r_pos)
            #     condition = True
            #     print("Right servo position: %s degrees", r_pos)

            sleep(1)   # May need more time to get the tilt sensors to stabilize
        print("Final servo positions: \n\tLeft: %s\n\tRight: %s", l_pos, r_pos)

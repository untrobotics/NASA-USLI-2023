import pigpio
from ..simple_servo.main import SimpleServo
from time import sleep

class DoorOpener:
    def __init__(self, left_servo_gpio, right_servo_gpio, tilt_sensor_l_gpio, tilt_sensor_r_gpio):
        self.l_servo = SimpleServo(left_servo_gpio)
        self.r_servo = SimpleServo(right_servo_gpio)
        self.tilt_sensor_l_gpio = tilt_sensor_l_gpio
        self.tilt_sensor_r_gpio = tilt_sensor_r_gpio
        self.pi = pigpio.pi()
        self.pi.set_mode(self.tilt_sensor_l_gpio, pigpio.INPUT)
        self.pi.set_mode(self.tilt_sensor_r_gpio, pigpio.INPUT)
        self.pi.set_mode(self.tilt_sensor_l_gpio, pigpio.PUD_DOWN)
        self.pi.set_mode(self.tilt_sensor_l_gpio, pigpio.PUD_DOWN)

    def open_doors(self):
        self.l_servo.set_position(50)
        self.r_servo.set_position(50)
        servo_current_pos = 50
        sleep(2)    # To allow time to get the things in position
        while not self.pi.read(self.tilt_sensor_l_gpio) and self.pi.read(self.tilt_sensor_r_gpio):
            self.l_servo.set_position(++servo_current_pos)
            self.r_servo.set_position(servo_current_pos)
            sleep(.5)   # May need more time to get the tilt sensors to stabilize


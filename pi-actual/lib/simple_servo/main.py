import pigpio
from time import sleep

class SimpleServo:
    pi = None
    control_gpio = None

    def __init__(self, control_gpio):
        print("(simple servo) control=", control_gpio)
        self.control_gpio = control_gpio
        self.pi = pigpio.pi()

    def set_position(self, degrees: int):
        self.pi.set_servo_pulsewidth(user_gpio=self.control_gpio, pulsewidth=SimpleServo.get_position(degrees))

    @staticmethod
    def get_position(degrees: int) -> float:
        if degrees < 0:
            degrees = 0
        elif degrees > 180:
            degrees = 180
        return degrees / 180 * 2000 + 500

if __name__ == '__main__':
    servo = Servo(23)
    servo.set_position(0)
    sleep(1)
    servo.set_position(180)

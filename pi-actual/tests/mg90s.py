import pigpio as pig

# This is the servo for popping the payload out of the rocket

class Servo:
    def __init__(self, pi, gpio_pin):
        self.pi = pi
        self.gpio_pin = gpio_pin

    def set_position(self, degrees: int):
        self.pi.set_servo_pulsewidth(user_gpio=self.gpio_pin, pulsewidth=Servo.calc_pulsewidth(degrees))

    @staticmethod
    def calc_pulsewidth(degrees: int) -> float:
        if degrees < 0:
            degrees = 0
        elif degrees > 180:
            degrees = 180
        return degrees / 180 * 2000 + 500


if __name__ == '__main__':
    pi = pig.pi()
    gpio = 26
    servo = Servo(pi, gpio)
    servo.set_position(0)
    while True:
        position = int(input("Enter position in degrees: "))
        servo.set_position(position)
        print("Position:", position)

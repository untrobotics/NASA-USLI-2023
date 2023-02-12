import lib_para_360_servo as lib_servo
import pigpio
from time import sleep

class Servo:
    CLOCKWISE = -1
    ANTI_CLOCKWISE = 1

    feedback = None
    control = None

    full_circle = 360
    duty_cycle_min = 27
    duty_cycle_max = 971

    default_speed = 1

    current_angle = None

    def __init__(self, control_gpio, feedback_gpio):
        pi = pigpio.pi()
        print("control=", control_gpio, ", feedback=", feedback_gpio)
        self.feedback = lib_servo.read_pwm(pi=pi,gpio=feedback_gpio)
        self.control = lib_servo.write_pwm(pi=pi,gpio=control_gpio)
        sleep(1) # give the servo time to initialise
        self.current_angle = self.get_angle(self.feedback.read())

    def get_angle(self, duty_cycle):
        if not duty_cycle: # if the duty cycle hasn't been calibrated yet, the duty_cycle will be None
            return 0

        angle = (self.full_circle - 1) - ((duty_cycle - self.duty_cycle_min) * self.full_circle) / (self.duty_cycle_max - self.duty_cycle_min + 1)
        angle = max(min((self.full_circle - 1), angle), 0)

        return angle

    def calc_target_angle_clockwise(self, degrees, current_angle):
        target_angle = current_angle + degrees
        if target_angle > 360:
            target_angle = target_angle - 360
        return target_angle

    def calc_target_angle_anti_clockwise(self, degrees, current_angle):
        target_angle = current_angle - degrees
        if target_angle < 0:
            target_angle = 360 + target_angle
        return target_angle

    def actuate(self, speed, multiplier = 1):
        self.control.set_speed(speed * multiplier)

    def rotate(self, direction, degrees):
        if direction == Servo.CLOCKWISE:
            target_angle = self.calc_target_angle_clockwise(degrees, self.current_angle)
            print("Rotating clockwise, from", self.current_angle, "to", target_angle)

        if direction == Servo.ANTI_CLOCKWISE:
            target_angle = self.calc_target_angle_anti_clockwise(degrees, self.current_angle)
            print("Rotating anti-clockwise, from", self.current_angle, "to", target_angle)

        self.actuate(self.default_speed, direction)

        while True:
            last_angle = self.current_angle
            self.current_angle = self.get_angle(self.feedback.read())

            # check for overflow, and overflow the last angle if necessary
            if direction == Servo.CLOCKWISE and self.current_angle < last_angle - 300:
                last_angle = 0

            if direction == Servo.ANTI_CLOCKWISE and self.current_angle > last_angle + 300:
                last_angle = 360

            if (direction == Servo.CLOCKWISE and self.current_angle >= target_angle and target_angle >= last_angle) or (direction == Servo.ANTI_CLOCKWISE and self.current_angle <= target_angle and target_angle <= last_angle):
                print("Final measured angle", self.current_angle)
                self.control.stop()
                break

if __name__ == '__main__':
    servo = Servo(12, 23)
    servo.rotate(Servo.ANTI_CLOCKWISE, 60)

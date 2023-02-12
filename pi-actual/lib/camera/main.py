from picamera2 import Picamera2
#from time import sleep

import datetime

class Camera:
    picam2 = None

    CLOCKWISE = -1
    ANTI_CLOCKWISE = 1

    feedback = None
    control = None

    full_circle = 360
    duty_cycle_min = 27
    duty_cycle_max = 971

    default_speed = 1

    current_angle = None

    def __init__(self):
        self.picam2 = Picamera2()
        camera_config = self.picam2.create_still_configuration()
        self.picam2.configure(camera_config)
        self.picam2.start()

    def capture(self):
        photo_filename = '/home/pi/capture/%s.jpg' % datetime.datetime.now()
        print("camera: taking picture, will place it at:", photo_filename)
        self.picam2.capture_file(photo_filename)

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

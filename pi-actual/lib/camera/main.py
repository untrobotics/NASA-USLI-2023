from picamera2 import Picamera2
#from time import sleep

import datetime

class Camera:
    picam2 = None

    mode = "colour";
    rotation = 0;
    filters = "none";

    def __init__(self):
        self.picam2 = Picamera2()
        camera_config = self.picam2.create_still_configuration()
        self.picam2.configure(camera_config)
        self.picam2.start()

    def capture(self):
        photo_filename = '/home/pi/capture/%s-mode:%s-rotation:%s-filters:%s.jpg' % (datetime.datetime.now(), self.mode, self.rotation, self.filters)
        print("camera: taking picture, will place it at:", photo_filename)
        self.picam2.capture_file(photo_filename)

    def to_grayscale(self):
        self.mode = "grayscale"

    def to_colour(self):
        self.mode = "colour"

    def rotate_image(self):
        self.rotation = 0 if self.rotation == 180 else 180

    def apply_sfx(self):
        self.filters = "invert"

    def remove_all_filters(self):
        self.filters = "none"

if __name__ == '__main__':
    camera = Camera()
    camera.capture()

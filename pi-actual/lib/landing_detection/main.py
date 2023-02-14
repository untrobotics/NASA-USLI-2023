from time import sleep
import board
import adafruit_bmp3xx
import adafruit_mpu6050
from collections import deque

class LandingDetection:
    agl_offset = None

    altitude_last_10 = deque([0 for i in range(10)])

    has_landed = False

    mpu = None #= adafruit_mpu6050.MPU6050(i2c, 0x69)
    bmp = None #= adafruit_bmp3xx.BMP3XX_I2C(i2c)

    def __init__(self):
       i2c = board.I2C()
       self.mpu = adafruit_mpu6050.MPU6050(i2c, 0x69) # short ad0 to ground
       self.bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
       self.calibrate()

    def calibrate(self):
        sleep(0.1)
        self.agl_offset = self.bmp.altitude

    def calculate_deltas(self, array):
        largest_delta = 0
        l = len(array)
        for i, x in enumerate(array):
            next_or_previous = i+1 if i < l-1 else 0
            delta = abs(x - array[next_or_previous])
            if delta > largest_delta:
                largest_delta = delta
        return largest_delta

    def detect_landing(self): # should be blocking
        print("----------------------")
        while not self.has_landed:
            # calculate details
            accel = self.mpu.acceleration
            gyro = self.mpu.gyro
            mpu_temperature = self.mpu.temperature
            altitude = self.bmp.altitude
            bmp_temperature = self.bmp.temperature
            height = altitude - self.agl_offset

            print("Accel: {}ms^-2, Gyro: {}rad/s, Alt: {}m, Height: {}m, T(MPU): {}C, T(BMP): {}C".format(accel, gyro, altitude, height, mpu_temperature, bmp_temperature))
            # check if height is less than 1m and has not changed significantly for 1s (10 iterations)
            self.altitude_last_10.popleft()
            self.altitude_last_10.append(altitude)
            delta = self.calculate_deltas(self.altitude_last_10)
            print("Deltas: {} ({})".format(delta, self.altitude_last_10))
            print("----------------------")

            if abs(delta) < 1 and height < 1:
                return
            sleep(0.1)

if __name__ == '__main__':
    landing_detection = LandingDetection()
    landing_detection.detect_landing()
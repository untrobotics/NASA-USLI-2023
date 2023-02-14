import time
import board
import adafruit_bmp3xx
import adafruit_mpu6050

def calibrate(sensor, threshold=50, n_samples=100):
    """
    Get calibration data for the sensor, by repeatedly measuring
    while the sensor is stable. The resulting calibration
    dictionary contains offsets for this sensor in its
    current position.
    """
    height = 0
    acceleration_x = 0
    acceleration_y = 0
    acceleration_z = 0
    print("CALIBRATING SENSOR")
    for i in range(n_samples):
        if sensor == 'bmp':
            data = bmp.altitude
            time.sleep(0.1)
            height+= data
    if sensor == 'bmp':
        data = height/n_samples
        return data
    else:
        print("Sensor not recognized")
        return None

    #while True:
     #   v1 = get_accel(n_samples)
     #   v2 = get_accel(n_samples)
        # Check all consecutive measurements are within
        # the threshold. We use abs() so all calculated
        # differences are positive.
     #   if all(abs(v1[k] - v2[k]) < threshold for k in v1.keys()):
     #       return v1  # Calibrated.

def get_smoothed_values(sensor, n_samples=10, calibration=None):
    """
    Get smoothed values from the sensor by sampling
    the sensor `n_samples` times and returning the mean.
    """
    result = {}
    for _ in range(n_samples):
        data = accel.get_values()

        for k in data.keys():
            # Add on value / n_samples (to generate an average)
            # with default of 0 for first loop.
            result[k] = result.get(k, 0) + (data[k] / n_samples)
    if calibration:
        # Remove calibration adjustment.
        for k in calibration.keys():
            result[k] -= calibration[k]

    return result

# i2c connection for mpu 6050
i2c = board.I2C()
mpu = adafruit_mpu6050.MPU6050(i2c, 0x69)
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

# bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

# SPI setup

#from digitalio import DigitalInOut, Direction
#import RPi.GPIO as GPIO
#import board
#spi = board.SPI()
#cs = DigitalInOut(board.D5)
#bmp = adafruit_bmp3xx.BMP3XX_SPI(spi, cs)



#bmp.reset()
#bmp.pressure_oversampling = 8 #for bmp390
#bmp.temperature_oversampling = 2
#time.sleep(2)
calibration_data = calibrate('bmp')
sea_level_feet = round(calibration_data, 2)

while True:
  #  data = get_smoothed_values(n_samples = 100, calibration = calibration)
  #  print(
  #      'Smooth \t'.join('{0}:{1:>10.1f}'.format(k, data[k])
  #      for k in sorted(data.keys())),end='\r')
    height_feet = bmp.altitude - sea_level_feet
    print(
#        "Pressure: {:6.4f} hPa Temperature: {:5.2f} C Altitude: {:5.4f} feet".format(bmp.pressure, bmp.temperature, height_feet)
    )
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f rad/s" % (mpu.gyro))
    print("Gyro Temperature: %.2f C" % mpu.temperature)
    print('Altitude: {} meters'.format(bmp.altitude))
    print("Temperature: {} U".format(bmp.temperature))
    print("Height: {} ft'".format(height_feet))
    time.sleep(1)
    #if height_feet < 5: #if less than 5 feet
    #    print("Rocket Near Land !!")

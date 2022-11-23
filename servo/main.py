import lib_para_360_servo as servoe
import pigpio as pig
from time import sleep
if __name__ == '__main__':
    pi = pig.pi()
    read1 = servoe.read_pwm(pi=pi,gpio=23)
    
    # Based off of BCM numbering (so GPIO 12 which is 32 in board pin numbering). On a pi zero, 12 and 13 are the pwm pins
    write1 = servoe.write_pwm(pi=pi,gpio=12)    
    write1.set_speed(1) # I don't know if this is clockwise or counter-clockwise, but -1 goes the opposite direction. Also speeds are between -1 and 1
    sleep(2)
    write1.set_speed(-1)
    sleep(2)
    write1.stop()

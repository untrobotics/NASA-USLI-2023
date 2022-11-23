import lib_para_360_servo as servoe
import pigpio as pig_pio
if __name__ == '__main__':
    pi = pig_pio.pi()
    read1 = servoe.read_pwm(pi=pi,gpio=23)
    write1 = servoe.write_pwm(pi=pi,gpio=12)
    write1.set_speed(1)
    write1.stop()

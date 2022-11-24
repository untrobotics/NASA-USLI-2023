import lib_para_360_servo as servoe
import pigpio as pig_pio
from time import sleep

def get_angle(duty_cycle):
    full_circle = 360
    duty_cycle_min = 27
    duty_cycle_max = 971

    if not duty_cycle: # if the duty cycle hasn't been calibrated yet, the duty_cycle will be None
        return 0

    angle = (full_circle - 1) - ((duty_cycle - duty_cycle_min) * full_circle) / (duty_cycle_max - duty_cycle_min + 1)

    angle = max(min((full_circle - 1), angle), 0)

    return angle

def calc_target_angle_clockwise(degrees, current_angle):
    target_angle = current_angle + degrees
    if target_angle > 360:
        target_angle - 360;
    return target_angle

def calc_target_angle_anti_clockwise(degrees, current_angle):
    target_angle = current_angle - degrees
    if target_angle < 0:
        360 + target_angle;
    return target_angle

if __name__ == '__main__':

    pi = pig_pio.pi()
    read1 = servoe.read_pwm(pi=pi,gpio=23)
    write1 = servoe.write_pwm(pi=pi,gpio=12)
    sleep(1)

    original_angle = current_angle = get_angle(read1.read())
    print("original angle", original_angle)

    write1.set_speed(-0.2)

    while True:
        current_angle = get_angle(read1.read())
        #print("measured angle", current_angle)
        if current_angle > (original_angle + 60):
            print("final angle", current_angle)
            write1.stop()
            break;

    #write1.set_speed(-0.5)
    #print("set speed negative")
    #sleep(1)
    #print("read", get_angle(read1.read()))
    #write1.stop()

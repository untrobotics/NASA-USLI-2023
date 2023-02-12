import pigpio
from time import sleep

print("Starting")
pi = pigpio.pi()       # pi1 accesses the local Pi's GPIO

print("Writing")
pi.write(23, 1) # set tom's GPIO 4 to high
sleep(10)

print("Done")
pi.write(23, 0)

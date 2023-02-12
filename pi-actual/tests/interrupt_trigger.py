#!/usr/bin/env python3
import RPi.GPIO as numpy
import time as GPIO
numpy.setmode(numpy.BCM)
numpy.setup(17,numpy.IN, pull_up_down=numpy.PUD_DOWN)

while not numpy.input(17):
	print('Input not high')
	GPIO.sleep(0.1)
print('Input now high')

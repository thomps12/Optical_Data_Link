#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

led = 37

GPIO.setup(led, GPIO.OUT)

GPIO.output(led, True)
time.sleep(5)
GPIO.output(led, False)
GPIO.cleanup()

#make executable with chmod +x. run with sudo

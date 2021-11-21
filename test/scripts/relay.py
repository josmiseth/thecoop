#!/usr/bin/env python

import time
from time import sleep
import RPi.GPIO as GPIO

print("starting test")
relay_pluss_up = 17
relay_minus_up = 5
relay_pluss_down = 6
relay_minus_down = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pluss_up, GPIO.OUT)
GPIO.setup(relay_minus_up, GPIO.OUT)
GPIO.setup(relay_pluss_down, GPIO.OUT)
GPIO.setup(relay_minus_down, GPIO.OUT)


GPIO.output(relay_pluss_up, GPIO.LOW)
GPIO.output(relay_minus_up, GPIO.LOW)


time.sleep(2.0)


GPIO.output(relay_pluss_up, GPIO.HIGH)
GPIO.output(relay_minus_up, GPIO.HIGH)
GPIO.output(relay_pluss_down, GPIO.LOW)
GPIO.output(relay_minus_down, GPIO.LOW)

time.sleep(2.0)

GPIO.output(relay_pluss_down, GPIO.HIGH)
GPIO.output(relay_minus_down, GPIO.HIGH)

time.sleep(2.0)




GPIO.cleanup()
print("test ended")

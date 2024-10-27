#!/usr/bin/env python


import time
from time import sleep
import RPi.GPIO as GPIO

import sys
sys.path.append('/home/josmi/projects/thecoop/')
import src as thecoop
from src.hatch_controller import limit_reached
from src.hatch_controller import open_hatch

GPIO.setup(thecoop.PIN_RED_LED, GPIO.OUT)

try:
    while True:
        if limit_reached(thecoop.PIN_LIMIT_UP):
            GPIO.output(thecoop.PIN_RED_LED, GPIO.HIGH)  # Turn LED on
            time.sleep(1)  # Keep it on for 1 second
            GPIO.output(thecoop.PIN_RED_LED, GPIO.LOW)   # Turn LED off
            time.sleep(1)  # Keep it off for 1 second

        if limit_reached(thecoop.PIN_LIMIT_DOWN):
            GPIO.output(thecoop.PIN_RED_LED, GPIO.HIGH)  # Turn LED on
            time.sleep(1)  # Keep it on for 1 second
            GPIO.output(thecoop.PIN_RED_LED, GPIO.LOW)   # Turn LED off
            time.sleep(1)  # Keep it off for 1 second
except KeyboardInterrupt:
    print("Program interrupted by user.")

finally:
    GPIO.cleanup()  # Clean up GPIO settings on exit

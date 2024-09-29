#!/usr/bin/env python


import time
from time import sleep
import RPi.GPIO as GPIO
import src as thecoop
from src.hatch_controller import limit_reached
from src.hatch_controller import open_hatch

GPIO.setmode(GPIO.BCM)                                           
GPIO.setup(thecoop.PIN_LIMIT_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP) # using the internal Pull up resistor

print("Limit reached: %s" % limit_reached(thecoop.PIN_LIMIT_UP))

open_hatch()
GPIO.cleanup()

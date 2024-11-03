#!/usr/bin/env python

'''

!!!   MAKE SURE HATCH IS PHYSICALLY CLOSED WHEN STARTING UP RASPBERRY PI  !!!



Relay wiring

Relay channel     Wire color     RB Port     Function
    4             Yellow         GPIO17      Minus wire hatch up
    3             Green          GPIO05      Plus wire hatch up
    2             Dark blue      GPIO06      Plus wire hatch down
    1             Pink           GPIO21      Minus wire hatch down

Push button wiring
Wire color        RB Port
Black             3.3 V (pin 1)
White             GPIO23

Temperature relay wiring
Brown             GPIO22


'''

import os
import logging
from src.hatch_controller import limit_reached

import RPi.GPIO as GPIO
import time

status_file_folder = "/tmp/thecoop"
status_file_name = "hatch_status.txt"

OPEN_HATCH_HOUR = 9
OPEN_HATCH_MINUTE = 0
CLOSE_HATCH_HOUR = 21
CLOSE_HATCH_MINUTE = 41

STATUS_CLOSED = '0'
STATUS_OPEN = '1'
STATUS_IN_MOTION = '2'
OPEN_HATCH_TIME_TO_RUN = 20.0 #0.7
CLOSE_HATCH_TIME_TO_RUN = 14.0 #0.5
#OPEN_HATCH_TIME_TO_RUN = 10.0 # Debug
#CLOSE_HATCH_TIME_TO_RUN = 10.0 # Debug


PIN_RED_LED = 27
PIN_LIMIT_UP = 16
PIN_LIMIT_DOWN = 20
PIN_RELAY_MINUS_UP = 17
PIN_RELAY_PLUS_UP = 5        
PIN_RELAY_PLUS_DOWN = 6
PIN_RELAY_MINUS_DOWN = 21
PIN_TEMP_RELAY = 22
PIN_PUSH_BUTTON = 23

LATITUDE = 63.446827
LONGITUDE = 10.421906

MINIMUM_TEMP = 4    # Degrees celcius

def set_hatch_status(filename):

    logger = logging.getLogger('hatch_logger')
    GPIO.output(PIN_RED_LED, GPIO.HIGH)  # Turn LED on


    if (limit_reached(PIN_LIMIT_UP)):
        status = STATUS_OPEN
        GPIO.output(PIN_RED_LED, GPIO.LOW)   # Turn LED off
        print("Status hatch open written to file")
        logger.info("Status hatch open written to file")
    elif(limit_reached(PIN_LIMIT_DOWN)):
        status = STATUS_CLOSED
        GPIO.output(PIN_RED_LED, GPIO.LOW)   # Turn LED off
        print("Status hatch closed written to file")
        logger.info("Status hatch closed written to file")
    else:
        print("Hatch position indecisive. Move to position fully open or fully closed")
        logger.error("Hatch position indecisive. Move to position fully open or fully closed")
        while True:
            GPIO.output(PIN_RED_LED, GPIO.HIGH)  # Turn LED on
            time.sleep(1)  # Keep it on for 1 second
            GPIO.output(PIN_RED_LED, GPIO.LOW)   # Turn LED off
            time.sleep(1)  # Keep it off for 1 second

    with open(filename, 'w') as file:
        file.write(status)
    return


def init_status_file_folder(folder):
    
    print("Setting up status file folder")
    # Create folder 
    if not os.path.exists(folder):
        os.mkdir(folder)
    
    return

def init_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='logging.log',
        filemode='w'
        )

    return


def init_pins():
    # Define the Pi pin numbering system
    GPIO.setmode(GPIO.BCM) 

    # set up internal pull resistors
    GPIO.setup(PIN_LIMIT_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_LIMIT_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_PUSH_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Set the red red pin as an output
    GPIO.setup(PIN_RED_LED, GPIO.OUT)

    return

# Set up logging
init_logging()


init_status_file_folder(status_file_folder)

# Initialize pins
init_pins()


#Create status text file
set_hatch_status(os.path.join(status_file_folder, status_file_name))

#Set led blinking status 
led_blinking = False

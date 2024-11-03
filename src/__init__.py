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
import pigpio
from time import sleep
from src.hatch_controller import limit_reached

pi = pigpio.pi()  # Initializes the pigpio interface

status_file_folder = "/tmp/thecoop"
status_file_name = "hatch_status.txt"

OPEN_HATCH_HOUR = 9
OPEN_HATCH_MINUTE = 0
CLOSE_HATCH_HOUR = 21
CLOSE_HATCH_MINUTE = 41

STATUS_CLOSED = '0'
STATUS_OPEN = '1'
STATUS_IN_MOTION = '2'
OPEN_HATCH_TIME_TO_RUN = 20.0
CLOSE_HATCH_TIME_TO_RUN = 14.0

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

MINIMUM_TEMP = 4    # Degrees Celsius

class HatchGPIO:
    def __init__(self):
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise RuntimeError("Failed to connect to pigpio daemon")
        
        # Initialize GPIO pins
        self.init_pins()

    def init_pins(self):
        # Set up pin modes
        self.pi.set_mode(PIN_LIMIT_UP, pigpio.INPUT)
        self.pi.set_mode(PIN_LIMIT_DOWN, pigpio.INPUT)
        self.pi.set_mode(PIN_PUSH_BUTTON, pigpio.INPUT)
        self.pi.set_mode(PIN_RED_LED, pigpio.OUTPUT)

        # Set pull-up resistors
        self.pi.set_pull_up_down(PIN_LIMIT_UP, pigpio.PUD_UP)
        self.pi.set_pull_up_down(PIN_LIMIT_DOWN, pigpio.PUD_UP)
        self.pi.set_pull_up_down(PIN_PUSH_BUTTON, pigpio.PUD_UP)

    def write_pin(self, pin, state):
        self.pi.write(pin, state)

    def read_pin(self, pin):
        return self.pi.read(pin)

    def cleanup(self):
        self.pi.stop()


def set_hatch_status(filename, gpio, pi):
    logger = logging.getLogger('hatch_logger')
    gpio.write_pin(PIN_RED_LED, 1)  # Turn LED on

    if limit_reached(pi, PIN_LIMIT_UP):
        status = STATUS_OPEN
        gpio.write_pin(PIN_RED_LED, 0)  # Turn LED off
        print("Status hatch open written to file")
        logger.info("Status hatch open written to file")
    elif limit_reached(pi, PIN_LIMIT_DOWN):
        status = STATUS_CLOSED
        gpio.write_pin(PIN_RED_LED, 0)  # Turn LED off
        print("Status hatch closed written to file")
        logger.info("Status hatch closed written to file")
    else:
        print("Hatch position indecisive. Move to position fully open or fully closed")
        logger.error("Hatch position indecisive. Move to position fully open or fully closed")
        while True:
            gpio.write_pin(PIN_RED_LED, 1)  # Turn LED on
            sleep(1)
            gpio.write_pin(PIN_RED_LED, 0)  # Turn LED off
            sleep(1)

    with open(filename, 'w') as file:
        file.write(status)
    return


def init_status_file_folder(folder):
    print("Setting up status file folder")
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


# Initialize logging and GPIO
init_logging()
gpio = HatchGPIO()

init_status_file_folder(status_file_folder)

# Create status text file
set_hatch_status(os.path.join(status_file_folder, status_file_name), gpio, pi)

# Set LED blinking status
led_blinking = False

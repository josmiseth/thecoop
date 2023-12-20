#!/usr/bin/env python

import time
import os
import sys
import logging
sys.path.append('/home/josmi/projects/thecoop/')


from apscheduler.schedulers.background import BackgroundScheduler
import src as thecoop


import time
from time import sleep
import RPi.GPIO as GPIO

from flask import Flask

def set_hatch_status(status, filename):
    
    with open(filename, 'w') as file:
        file.write(status)
    return


def get_hatch_status(filename):
    
    with open(filename, 'r') as file:
        status = file.read()    
    return status

def is_hightemp():
    logger = logging.getLogger('hatch_logger')
    logger.info("probing temperature")
    print("Probing temperature")
    
    state = False
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(thecoop.PIN_TEMP_RELAY, GPIO.IN)
        state = GPIO.input(thecoop.PIN_TEMP_RELAY)
    finally:
        print("")
        
    if state:
        logger.info("Temperature is above set minimum temperature")
        print("High temperature")
    else:
        logger.info("Temperature is below set minimum temperature")
        print("Low temperature")
    return state

def open_hatch_run():
    logger = logging.getLogger('hatch_logger')

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(thecoop.PIN_RELAY_PLUS_UP, GPIO.OUT)
    GPIO.setup(thecoop.PIN_RELAY_MINUS_UP, GPIO.OUT)

    logger.info("Hatch in motion")
    #Save hatch status running to file
    set_hatch_status(thecoop.STATUS_IN_MOTION, os.path.join(thecoop.status_file_folder, thecoop.status_file_name))
    
    GPIO.output(thecoop.PIN_RELAY_PLUS_UP, GPIO.LOW)
    GPIO.output(thecoop.PIN_RELAY_MINUS_UP, GPIO.LOW)

    time.sleep(thecoop.OPEN_HATCH_TIME_TO_RUN)
    
    GPIO.output(thecoop.PIN_RELAY_PLUS_UP, GPIO.HIGH)
    GPIO.output(thecoop.PIN_RELAY_MINUS_UP, GPIO.HIGH)


    #Save hatch status open to file
    set_hatch_status(thecoop.STATUS_OPEN, os.path.join(thecoop.status_file_folder, thecoop.status_file_name))
    print("Hatch open\n\n")
    logger.info("Hatch open")

    return

def open_hatch():
    logger = logging.getLogger('hatch_logger')
    print("Event: Open hatch")
    logger.info("Event: Open hatch")
    
    # First, check if hatch is open. Is , do not open
    print("Checking hatch status")
    if get_hatch_status(os.path.join(thecoop.status_file_folder, thecoop.status_file_name)) != thecoop.STATUS_CLOSED:
        logger.warning("Hatch is not closed, not proceding with opening hatch")
    elif not is_hightemp():
    # Check if temperature is too low
        logger.info("Temperature is low. Hatch not opening")
        print("Temperature is low. Hatch not opening")
    else:
        open_hatch_run()

    return


def close_hatch():
    logger = logging.getLogger('hatch_logger')

    print("Event: Close hatch")
    logger.info("Event: Close hatch")

    # First, check if hatch is closed. Is , do not close
    print("Checking hatch status")
    if get_hatch_status(os.path.join(thecoop.status_file_folder, thecoop.status_file_name)) != thecoop.STATUS_OPEN:
        logger.warning("Hatch is not open, not proceding with closing hatch")
    else:
    
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(thecoop.PIN_RELAY_PLUS_DOWN, GPIO.OUT)
        GPIO.setup(thecoop.PIN_RELAY_MINUS_DOWN, GPIO.OUT)

        #Save hatch status running to file
        set_hatch_status(thecoop.STATUS_IN_MOTION, os.path.join(thecoop.status_file_folder, thecoop.status_file_name))

        GPIO.output(thecoop.PIN_RELAY_PLUS_DOWN, GPIO.LOW)
        GPIO.output(thecoop.PIN_RELAY_MINUS_DOWN, GPIO.LOW)

        time.sleep(thecoop.CLOSE_HATCH_TIME_TO_RUN)
        
        GPIO.output(thecoop.PIN_RELAY_PLUS_DOWN, GPIO.HIGH)
        GPIO.output(thecoop.PIN_RELAY_MINUS_DOWN, GPIO.HIGH)
        #Save hatch status open to file
        set_hatch_status(thecoop.STATUS_CLOSED, os.path.join(thecoop.status_file_folder, thecoop.status_file_name))

        print("Hatch closed\n\n")
        logger.info("Hatch closed")

    return

def button_pushed(channel):
    print("Button pushed")
    logger = logging.getLogger('hatch_logger')
    logger.info("Event: Button pushed")
    
    hatch_status = get_hatch_status(os.path.join(thecoop.status_file_folder, thecoop.status_file_name))
    
    if GPIO.input(channel) == GPIO.HIGH:
        if hatch_status == thecoop.STATUS_CLOSED:
            print("Checking hatch status")
            if get_hatch_status(os.path.join(thecoop.status_file_folder, thecoop.status_file_name)) != thecoop.STATUS_CLOSED:
                logger.warning("Hatch is not closed, not proceding with opening hatch")
            else:
                logger.info("Open hatch")
                open_hatch_run()       
        elif hatch_status == thecoop.STATUS_OPEN:
            logger.info("Close hatch")
            close_hatch()
        elif hatch_status == thecoop.STATUS_IN_MOTION:
            logger.waring("Hatch in motion. Doing nothing to change that")
    logger.info("End button pushed\n")
        
        
def start_controller():
    
    logger = logging.getLogger('hatch_logger')
    logger.info("Starting logger")
    logger.info("Setting up background scheduler")
    sched = BackgroundScheduler()


    logger.info("Adding cron job")
    sched.add_job(open_hatch, 'cron', hour=21, minute=17)
    sched.add_job(close_hatch, 'cron', hour=21, minute=18)

    sched.print_jobs()
    
    print("Starting cron job")
    sched.start()


    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(thecoop.PIN_PUSH_BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.add_event_detect(thecoop.PIN_PUSH_BUTTON, GPIO.RISING, callback=button_pushed)

        while True:
            time.sleep(10)


    finally:
        print("clean up")
        GPIO.cleanup() # cleanup all GPIO


    sched.shutdown()


# Main script starting here

if __name__ == '__main__':
    print("Start main script")

    print("Init package from __init__.py")
    print("\n \n MAKE SURE HATCH IS PHYSICALLY CLOSED WHEN STARTING UP RASPBERRY PI \n \n")


    start_controller()

#!/usr/bin/env python

import time
import os
import sys
sys.path.append('/home/pi/projects/thecoop/')

from apscheduler.schedulers.background import BackgroundScheduler
from src import open_hatch
import src as thecoop


import time
from time import sleep
import RPi.GPIO as GPIO


def set_hatch_status(status, filename):
    
    with open(filename, 'w') as file:
        file.write(status)
    return


def get_hatch_status(filename):
    
    with open(filename, 'r') as file:
        status = file.read()    
    return status

def is_hightemp():
    print("probing temperature")
    state = False
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(thecoop.PIN_TEMP_RELAY, GPIO.IN)
        state = GPIO.input(thecoop.PIN_TEMP_RELAY)
    finally:
        print("")
        
    if state:
        print("Temperature is above set minimum temperature")
    else:
        print("Temperature is below set minimum temperature")
    return state

def open_hatch():

    print("Event: Open hatch")
    

    # First, check if hatch is open. Is , do not open
    print("Checking hatch status")
    if get_hatch_status(os.path.join(thecoop.status_file_folder, thecoop.status_file_name)) != thecoop.STATUS_CLOSED:
        print("Hatch is not closed, not proceding with opening hatch")
    elif not is_hightemp():
    # Check if temperature is too low
        print("Temperature is low. Hatch not opening")
    else:

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(thecoop.PIN_RELAY_PLUS_UP, GPIO.OUT)
        GPIO.setup(thecoop.PIN_RELAY_MINUS_UP, GPIO.OUT)

        print("Hatch in motion")
        #Save hatch status running to file
        set_hatch_status(thecoop.STATUS_IN_MOTION, os.path.join(thecoop.status_file_folder, thecoop.status_file_name))

        GPIO.output(thecoop.PIN_RELAY_PLUS_UP, GPIO.LOW)
        GPIO.output(thecoop.PIN_RELAY_MINUS_UP, GPIO.LOW)

        time.sleep(thecoop.OPEN_HATCH_TIME_TO_RUN)

        #Save hatch status open to file
        set_hatch_status(thecoop.STATUS_OPEN, os.path.join(thecoop.status_file_folder, thecoop.status_file_name))
        print("Hatch open\n\n")

    return


def close_hatch():

    print("Event: Close hatch")


    # First, check if hatch is closed. Is , do not close
    print("Checking hatch status")
    if get_hatch_status(os.path.join(thecoop.status_file_folder, thecoop.status_file_name)) != thecoop.STATUS_OPEN:
        print("Hatch is not open, not proceding with closing hatch")
    else:
    
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(thecoop.PIN_RELAY_PLUS_DOWN, GPIO.OUT)
        GPIO.setup(thecoop.PIN_RELAY_MINUS_DOWN, GPIO.OUT)

        #Save hatch status running to file
        set_hatch_status(thecoop.STATUS_IN_MOTION, os.path.join(thecoop.status_file_folder, thecoop.status_file_name))

        GPIO.output(thecoop.PIN_RELAY_PLUS_DOWN, GPIO.LOW)
        GPIO.output(thecoop.PIN_RELAY_MINUS_DOWN, GPIO.LOW)

        time.sleep(thecoop.CLOSE_HATCH_TIME_TO_RUN)

        #Save hatch status open to file
        set_hatch_status(thecoop.STATUS_CLOSED, os.path.join(thecoop.status_file_folder, thecoop.status_file_name))

        print("Hatch closed\n\n")

    return

def button_pushed(channel):
    print("Button pushed")
    
    hatch_status = get_hatch_status(os.path.join(thecoop.status_file_folder, thecoop.status_file_name))
    
    if GPIO.input(channel) == GPIO.HIGH:
        if hatch_status == thecoop.STATUS_CLOSED:
            print("Open hatch")
            open_hatch()       
        elif hatch_status == thecoop.STATUS_OPEN:
            print("Close hatch")
            close_hatch()
        elif hatch_status == thecoop.STATUS_IN_MOTION:
            print("Hatch in motion. Doing nothing to change that")
    print("End button pushed\n")
        
        
# Main script starting here

print("Setting up background scheduler")
sched = BackgroundScheduler()

print("Adding cron job")
sched.add_job(open_hatch, 'cron', hour=19, minute=52)
sched.add_job(close_hatch, 'cron', hour=19, minute=53)


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


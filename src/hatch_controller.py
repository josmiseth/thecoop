#!/usr/bin/env python

import time
import os
import sys
sys.path.append('/home/pi/projects/thecoop/')

from apscheduler.schedulers.background import BackgroundScheduler
from src import open_hatch
import src as thecoop


'''
Relay wiring

Relay channel     Wire color     RB Port     Function
    4             Yellow         GPIO17      Minus wire hatch up
    3             Green          GPIO05      Plus wire hatch up
    2             Dark blue      GPIO06      Plus wire hatch down
    1             Blue           GPIO07      Minus wire hatch down

'''

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
        GPIO.setup(18, GPIO.IN)
        state = GPIO.input(18)
    
 
    finally:
        GPIO.cleanup()
        
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
    
    
        relay_minus_up = 17
        relay_plus_up = 5
        time_to_run = 10.0


        GPIO.setmode(GPIO.BCM)
        GPIO.setup(relay_plus_up, GPIO.OUT)
        GPIO.setup(relay_minus_up, GPIO.OUT)

        print("Hatch in motion")
        #Save hatch status running to file
        set_hatch_status(thecoop.STATUS_IN_MOTION, os.path.join(thecoop.status_file_folder, thecoop.status_file_name))

        GPIO.output(relay_plus_up, GPIO.LOW)
        GPIO.output(relay_minus_up, GPIO.LOW)

        time.sleep(time_to_run)


        GPIO.cleanup()

        #Save hatch status open to file
        #Save hatch status running to file
        set_hatch_status(thecoop.STATUS_OPEN, os.path.join(thecoop.status_file_folder, thecoop.status_file_name))
        print("Hatch open")

    print("Open hatch finished")
    return


def close_hatch():

    print("Event: Close hatch")
    
    # First, check if hatch is closed. Is , do not close
    print("Checking hatch status")
    if get_hatch_status(os.path.join(thecoop.status_file_folder, thecoop.status_file_name)) != thecoop.STATUS_OPEN:
        print("Hatch is not open, not proceding with closing hatch")
    else:
    
    
        print("Hatch closed")

    print("Close hatch finished")
    return

#Initialize (create statusfile)

print("Setting up background scheduler")
sched = BackgroundScheduler()

print("Adding cron job")
sched.add_job(open_hatch, 'cron', hour=17, minute=12)
sched.add_job(close_hatch, 'cron', hour=17, minute=13)


print("Starting cron job")
sched.start()

while True:
    time.sleep(10)
sched.shutdown()

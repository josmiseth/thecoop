#!/usr/bin/env python

import time
import datetime
from suntime import Sun, SunTimeException
import calendar

import os
import sys
import logging
sys.path.append('/home/josmi/projects/thecoop/')

import requests

from apscheduler.schedulers.background import BackgroundScheduler
import src as thecoop


import time
from time import sleep
import RPi.GPIO as GPIO

from flask import Flask

def limit_reached(pin_number):
    
    #print("Check if limit reached (switch pushed)")
    
    state = False
    try:
        state = not GPIO.input(pin_number)
        # print("Pin state: ")
        # print(state)
    except:
        logging.info("Error with pin when testing limit switch")

    return state


def set_hatch_status(status, filename):
    
    with open(filename, 'w') as file:
        file.write(status)

    logging.info("Status file written: %s" % status)
    url_remote="http://10.0.0.54:8080/water-tank/insert_hatch_data.php?status=" + str(status)
    cmd="curl -s " + url_remote
    result=os.popen(cmd).read()
    logging.info(cmd)

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
        logger.info("Temperature pin state: ")
        logger.info(state)
    finally:
        print("")
        
    if state:
        logger.info("Temperature is above set minimum temperature")
        print("High temperature")
    else:
        logger.info("Relay indicating temperature below set minimum temperature")
        print("Relay indicating low temperature")

        print("Checking weatherforecast in case of failed temperature measurement")
        logger.info("Checking weatherforecast in case of failed temperature measurement")

        latitude = thecoop.LATITUDE
        longitude = thecoop.LONGITUDE

        url =  'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=%1.4f&lon=%1.4f' % (latitude, longitude)


        headers = {
            'User-Agent': 'theCoop github.com/josmiseth/thecoop.git',
        }

        #TODO: add try here
        
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            met_data = response.json()
            instant_temperature = met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"]
            
            if instant_temperature <= thecoop.MINIMUM_TEMP:
                state = False
                logger.info("Met weatherforecast instant temperature %1.2f is less than minimum temp %1.2f" % (instant_temperature, thecoop.MINIMUM_TEMP))
                print("Met weatherforecast instant temperature %1.2f is less than minimum temp %1.2f" % (instant_temperature, thecoop.MINIMUM_TEMP))

            else:
                logger.info("Met weatherforecast instant temperature %1.2f higher than minimum temp %1.2f" % (instant_temperature, thecoop.MINIMUM_TEMP))
                print("Met weatherforecast instant temperature %1.2f higher than minimum temp %1.2f" % (instant_temperature, thecoop.MINIMUM_TEMP))

                state = True
        
    return state

def open_hatch_run():
    logger = logging.getLogger('hatch_logger')

    checkloops = 100
    delta_t = thecoop.OPEN_HATCH_TIME_TO_RUN/checkloops

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(thecoop.PIN_RELAY_PLUS_UP, GPIO.OUT)
    GPIO.setup(thecoop.PIN_RELAY_MINUS_UP, GPIO.OUT)

    logger.info("Hatch in motion")
    #Save hatch status running to file
    set_hatch_status(thecoop.STATUS_IN_MOTION, os.path.join(thecoop.status_file_folder, thecoop.status_file_name))
    
    GPIO.output(thecoop.PIN_RELAY_PLUS_UP, GPIO.LOW)
    GPIO.output(thecoop.PIN_RELAY_MINUS_UP, GPIO.LOW)

    timepassed = 0
    while not limit_reached(thecoop.PIN_LIMIT_UP) and timepassed < thecoop.OPEN_HATCH_TIME_TO_RUN:
        time.sleep(delta_t)
        timepassed = timepassed + delta_t

    #time.sleep(thecoop.OPEN_HATCH_TIME_TO_RUN)
    
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

    checkloops = 100
    delta_t = thecoop.CLOSE_HATCH_TIME_TO_RUN/checkloops

    
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

        timepassed = 0
        while not limit_reached(thecoop.PIN_LIMIT_DOWN) and timepassed < thecoop.CLOSE_HATCH_TIME_TO_RUN:
            time.sleep(delta_t)
            timepassed = timepassed + delta_t

        #time.sleep(thecoop.CLOSE_HATCH_TIME_TO_RUN)

        
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

    logger.info("Setting up sun with local coordinates")
    sun = Sun(thecoop.LATITUDE, thecoop.LONGITUDE)

    logger.info("Setting up background scheduler")
    sched = BackgroundScheduler()


    logger.info("Adding open hatch cron job")
    sched.add_job(open_hatch, 'cron', hour=thecoop.OPEN_HATCH_HOUR, minute=thecoop.OPEN_HATCH_MINUTE)

    logger.info("Get current year to set up cron schedule")
    today = datetime.date.today()
    currentyear = today.year
    
    logger.info("Setting up close hatch cron jobs for each day 1 hour after sunset")
    #Setting up dates times for sunset for all days in a leap year (2024)
    for month in range(1,13):
        for day in range(1,calendar.monthrange(currentyear, month)[1]+1):
            date = datetime.date(currentyear, month, day)
            sunset = sun.get_local_sunset_time(date)
            sunset_plus_one_hour = sunset + datetime.timedelta(hours=1)
            hour = sunset_plus_one_hour.strftime('%H')
            minute = sunset_plus_one_hour.strftime('%M')

            sched.add_job(close_hatch, 'cron', month=month, day=day, hour=hour, minute=minute)

    #sched.add_job(close_hatch, 'cron', hour=thecoop.CLOSE_HATCH_HOUR, minute=thecoop.CLOSE_HATCH_TIME_TO_RUN)

    sched.print_jobs()
    
    logger.info("Starting cron job")
    sched.start()


    try:
        GPIO.setmode(GPIO.BCM)
#        GPIO.setup(thecoop.PIN_PUSH_BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(thecoop.PIN_PUSH_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.setup(thecoop.PIN_LIMIT_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP) # using the internal Pull up resistor
        GPIO.setup(thecoop.PIN_LIMIT_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # using the internal Pull up resistor
        
        GPIO.add_event_detect(thecoop.PIN_PUSH_BUTTON, GPIO.RISING, callback=button_pushed, bouncetime=300)

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

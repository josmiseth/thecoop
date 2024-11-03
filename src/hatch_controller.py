#!/usr/bin/env python

import time
import datetime
from suntime import Sun
import calendar
import os
import sys
import logging
sys.path.append('/home/josmi/projects/thecoop/')

import requests
import threading
from apscheduler.schedulers.background import BackgroundScheduler
import src as thecoop
from flask import Flask
import pigpio

def limit_reached(pi, pin_number):
    try:
        state = not pi.read(pin_number)
    except Exception as e:
        logging.info(f"Error with pin when testing limit switch: {e}")
        state = False
    return state

def set_hatch_status(status, filename):
    with open(filename, 'w') as file:
        file.write(status)
    logging.info(f"Status file written: {status}")
    url_remote = f"http://10.0.0.54:8080/water-tank/insert_hatch_data.php?status={status}"
    cmd = f"curl -s {url_remote}"
    result = os.popen(cmd).read()
    logging.info(cmd)

def get_hatch_status(filename):
    with open(filename, 'r') as file:
        status = file.read()    
    return status

def is_hightemp(pi):
    logger = logging.getLogger('hatch_logger')
    logger.info("Probing temperature")
    
    try:
        state = pi.read(thecoop.PIN_TEMP_RELAY)
        logger.info(f"Temperature pin state: {state}")
    except Exception as e:
        logger.error(f"Temperature check failed: {e}")
        state = False

    if not state:
        latitude, longitude = thecoop.LATITUDE, thecoop.LONGITUDE
        url = f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={latitude}&lon={longitude}'
        headers = {'User-Agent': 'theCoop github.com/josmiseth/thecoop.git'}
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            met_data = response.json()
            instant_temperature = met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"]
            state = instant_temperature > thecoop.MINIMUM_TEMP
            logger.info(f"Temperature: {instant_temperature}°C")
    return state

def open_hatch_run(pi):
    logger = logging.getLogger('hatch_logger')
    delta_t = thecoop.OPEN_HATCH_TIME_TO_RUN / 100
    pi.write(thecoop.PIN_RELAY_PLUS_UP, 0)
    pi.write(thecoop.PIN_RELAY_MINUS_UP, 0)
    
    set_hatch_status(thecoop.STATUS_IN_MOTION, os.path.join(thecoop.status_file_folder, thecoop.status_file_name))
    
    timepassed = 0
    while not limit_reached(pi, thecoop.PIN_LIMIT_UP) and timepassed < thecoop.OPEN_HATCH_TIME_TO_RUN:
        time.sleep(delta_t)
        timepassed += delta_t
    
    pi.write(thecoop.PIN_RELAY_PLUS_UP, 1)
    pi.write(thecoop.PIN_RELAY_MINUS_UP, 1)
    set_hatch_status(thecoop.STATUS_OPEN, os.path.join(thecoop.status_file_folder, thecoop.status_file_name))
    logger.info("Hatch open")

def open_hatch(pi):
    logger = logging.getLogger('hatch_logger')
    if get_hatch_status(os.path.join(thecoop.status_file_folder, thecoop.status_file_name)) != thecoop.STATUS_CLOSED:
        logger.warning("Hatch is not closed, not proceeding with opening hatch")
    elif not is_hightemp(pi):
        logger.info("Temperature is low. Hatch not opening")
    else:
        open_hatch_run(pi)

def close_hatch(pi):
    logger = logging.getLogger('hatch_logger')
    delta_t = thecoop.CLOSE_HATCH_TIME_TO_RUN / 100
    pi.write(thecoop.PIN_RELAY_PLUS_DOWN, 0)
    pi.write(thecoop.PIN_RELAY_MINUS_DOWN, 0)

    set_hatch_status(thecoop.STATUS_IN_MOTION, os.path.join(thecoop.status_file_folder, thecoop.status_file_name))

    timepassed = 0
    while not limit_reached(pi, thecoop.PIN_LIMIT_DOWN) and timepassed < thecoop.CLOSE_HATCH_TIME_TO_RUN:
        time.sleep(delta_t)
        timepassed += delta_t

    pi.write(thecoop.PIN_RELAY_PLUS_DOWN, 1)
    pi.write(thecoop.PIN_RELAY_MINUS_DOWN, 1)
    set_hatch_status(thecoop.STATUS_CLOSED, os.path.join(thecoop.status_file_folder, thecoop.status_file_name))
    logger.info("Hatch closed")

def button_pushed(channel, pi):
    global led_blinking
    logger = logging.getLogger('hatch_logger')
    logger.info("Event: Button pushed")
    
    led_blinking = True
    led_thread = threading.Thread(target=blink_led, args=(pi,))
    led_thread.start()

    hatch_status = get_hatch_status(os.path.join(thecoop.status_file_folder, thecoop.status_file_name))
    if hatch_status == thecoop.STATUS_CLOSED:
        open_hatch(pi)
    elif hatch_status == thecoop.STATUS_OPEN:
        close_hatch(pi)

    led_blinking = False
    time.sleep(2.0)

def blink_led(pi):
    global led_blinking
    while led_blinking:
        pi.write(thecoop.PIN_RED_LED, 1)
        time.sleep(0.5)
        pi.write(thecoop.PIN_RED_LED, 0)
        time.sleep(0.5)

def start_controller():
    logger = logging.getLogger('hatch_logger')
    pi = pigpio.pi()
    if not pi.connected:
        raise RuntimeError("Failed to connect to pigpio daemon")

    sun = Sun(thecoop.LATITUDE, thecoop.LONGITUDE)
    sched = BackgroundScheduler()
    sched.add_job(lambda: open_hatch(pi), 'cron', hour=thecoop.OPEN_HATCH_HOUR, minute=thecoop.OPEN_HATCH_MINUTE)

    today = datetime.date.today()
    for month in range(1, 13):
        for day in range(1, calendar.monthrange(today.year, month)[1] + 1):
            sunset = sun.get_local_sunset_time(datetime.date(today.year, month, day)) + datetime.timedelta(hours=1)
            sched.add_job(lambda: close_hatch(pi), 'cron', month=month, day=day, hour=sunset.hour, minute=sunset.minute)

    sched.start()
    try:
        pi.set_mode(thecoop.PIN_PUSH_BUTTON, pigpio.INPUT)
        pi.set_pull_up_down(thecoop.PIN_PUSH_BUTTON, pigpio.PUD_UP)
        pi.callback(thecoop.PIN_PUSH_BUTTON, pigpio.RISING_EDGE, lambda g, l, t: button_pushed(thecoop.PIN_PUSH_BUTTON, pi))
        while True:
            time.sleep(0.25)
    finally:
        pi.stop()
        sched.shutdown()

if __name__ == '__main__':
    start_controller()

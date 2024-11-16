#!/usr/bin/env python

import time
import datetime
from suntime import Sun
import calendar
import os
import sys
import logging
sys.path.append('/home/josmi/projects/thecoop/')
import src as thecoop

import requests
import threading
from apscheduler.schedulers.background import BackgroundScheduler

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

        # Get current date and set target timestamp at 13:00 UTC
        current_date = datetime.utcnow().strftime('%Y-%m-%d')
        target_timestamp = f"{current_date}T13:00:00Z"

        latitude, longitude = thecoop.LATITUDE, thecoop.LONGITUDE
        url = f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={latitude}&lon={longitude}'
        headers = {'User-Agent': 'theCoop github.com/josmiseth/thecoop.git'}
        
        state = True  # Default to "yes" if an exception occurs

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)

            try:
                met_data = response.json()
                try:
                    time_data = met_data["properties"]["timeseries"]
                    # Extract the record matching the target timestamp
                    record = next((item for item in time_data if item['time'] == target_timestamp), None)
                    if record:
                        day_temp = record["data"]["instant"]["details"]["air_temperature"]
                        state = day_temp > thecoop.MINIMUM_TEMP
                        logging.info(f"Day temperature forecast: {day_temp}°C")
                    else:
                        logging.info("No record found for 13:00 UTC on the current date.")
                        logging.info("Trying to use instant temperature")
                        instant_temperature = met_data["properties"]["timeseries"][0]["data"]["instant"]["details"]["air_temperature"]
                        state = instant_temperature > thecoop.MINIMUM_TEMP
                        logger.info(f"Temperature: {instant_temperature}°C")
                except (KeyError, IndexError) as e:
                    logger.error(f"Error accessing temperature data: {e}")
            except ValueError as e:
                logger.error(f"Error decoding JSON response: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP request failed: {e}")

        # state will remain True if any exception is thrown. So, if the met.no api fails the hatch will open
    return state

def open_hatch_run(pi):
    global led_blinking
    led_blinking = True
    led_thread = threading.Thread(target=blink_led, args=(pi,))
    led_thread.start()

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
    led_blinking = False

def open_hatch(pi):
    logger = logging.getLogger('hatch_logger')
    if get_hatch_status(os.path.join(thecoop.status_file_folder, thecoop.status_file_name)) != thecoop.STATUS_CLOSED:
        logger.warning("Hatch is not closed, not proceeding with opening hatch")
    elif not is_hightemp(pi):
        logger.info("Temperature is low. Hatch not opening")
    else:
        open_hatch_run(pi)

def close_hatch(pi):
    global led_blinking
    
    logger = logging.getLogger('hatch_logger')

    led_blinking = True
    led_thread = threading.Thread(target=blink_led, args=(pi,))
    led_thread.start()

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
    led_blinking = False

def button_pushed(channel, pi):
    global led_blinking
    logger = logging.getLogger('hatch_logger')
    logger.info("Event: Button pushed")
    
    led_blinking = True
    led_thread = threading.Thread(target=blink_led, args=(pi,))
    led_thread.start()

    hatch_status = get_hatch_status(os.path.join(thecoop.status_file_folder, thecoop.status_file_name))

    led_blinking = False

    if hatch_status == thecoop.STATUS_CLOSED:
        open_hatch_run(pi)
    elif hatch_status == thecoop.STATUS_OPEN:
        close_hatch(pi)

    
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

    sched.print_jobs()
    sched.start()
    try:
        pi.set_mode(thecoop.PIN_PUSH_BUTTON, pigpio.INPUT)
        pi.set_pull_up_down(thecoop.PIN_PUSH_BUTTON, pigpio.PUD_UP)
        pi.callback(thecoop.PIN_PUSH_BUTTON, pigpio.RISING_EDGE, lambda g, l, t: button_pushed(thecoop.PIN_PUSH_BUTTON, pi))
        while True:
            time.sleep(1)
    finally:
        pi.stop()
        sched.shutdown()

if __name__ == '__main__':
    start_controller()

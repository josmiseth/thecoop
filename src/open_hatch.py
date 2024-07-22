#!/usr/bin/env python


'''
Relay wiring

Relay channel     Wire color     RB Port     Function
    4             Yellow         GPIO17      Minus wire hatch up
    3             Green          GPIO05      Plus wire hatch up
    2             Dark blue      GPIO06      Plus wire hatch down
    1             Blue           GPIO21      Minus wire hatch down

Limit switch
RB Port
GPIO16

'''

import time
from time import sleep
import RPi.GPIO as GPIO

def limit_reached():
    
    # print("Check if limit reached (switch pushed)")
    
    state = False
    try:
        state = not GPIO.input(16)
        # print("Pin state: ")
        # print(state)
    except:
        print("Error with pin")

    return state



def print_text():
    print("Scheduled event")
    
    return

def set_hatch_status(status, filename):
    
    with open(filename, 'w') as file:
        file.write(status)
    return

def open_hatch():

    print("Open hatch")
    relay_minus_up = 17
    relay_plus_up = 5
    time_to_run = 2.0
    checkloops = 100
    delta_t = time_to_run/checkloops
    state_file_name = "/tmp/thecoop/hatch_status.txt"


    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay_plus_up, GPIO.OUT)
    GPIO.setup(relay_minus_up, GPIO.OUT)

    #Save hatch status running to file
 #   set_hatch_status("in_motion", state_file_name)

    GPIO.output(relay_plus_up, GPIO.LOW)
    GPIO.output(relay_minus_up, GPIO.LOW)

    
    while not limit_reached():
        time.sleep(delta_t)

    print("Limit switch reached")
    GPIO.output(relay_plus_up, GPIO.HIGH)
    GPIO.output(relay_minus_up, GPIO.HIGH)

    time.sleep(time_to_run)
    #Save hatch status open to file
    #Save hatch status running to file
#    set_hatch_status("open", state_file_name)

    print("Open hatch finished")
    return



GPIO.setmode(GPIO.BCM)     
pushpin = 16                                        
GPIO.setup(pushpin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # using the internal Pull up resistor

print(limit_reached())


open_hatch()
print("End")
GPIO.cleanup()

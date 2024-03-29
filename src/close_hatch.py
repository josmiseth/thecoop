#!/usr/bin/env python

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

print("Close hatch")
relay_plus_down = 6
relay_minus_down = 7
time_to_run = 10.0
state_file_name = "/tmp/thecoop/hatch_status.txt"

def set_hatch_status(status, filename):
    
    with open(filename, 'w') as file:
        file.write(status)

GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_plus_down, GPIO.OUT)
GPIO.setup(relay_minus_down, GPIO.OUT)

#Save hatch status running to file
set_hatch_status("in_motion", state_file_name)

GPIO.output(relay_plus_down, GPIO.LOW)
GPIO.output(relay_minus_down, GPIO.LOW)

time.sleep(time_to_run)


GPIO.cleanup()

#Save hatch status open to file
#Save hatch status running to file
set_hatch_status("closed", state_file_name)

print("Close hatch finished")

exit()
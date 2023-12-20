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

status_file_folder = "/tmp/thecoop"
status_file_name = "hatch_status.txt"

OPEN_HATCH_HOUR = 21
OPEN_HATCH_MINUTE = 40
CLOSE_HATCH_HOUR = 21
CLOSE_HATCH_MINUTE = 41

STATUS_CLOSED = '0'
STATUS_OPEN = '1'
STATUS_IN_MOTION = '2'
OPEN_HATCH_TIME_TO_RUN = 3
CLOSE_HATCH_TIME_TO_RUN = 3

PIN_RELAY_MINUS_UP = 17
PIN_RELAY_PLUS_UP = 5        
PIN_RELAY_PLUS_DOWN = 6
PIN_RELAY_MINUS_DOWN = 21
PIN_TEMP_RELAY = 22
PIN_PUSH_BUTTON = 23


def set_hatch_status(status, filename):
    
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

# Set up logging
init_logging()


init_status_file_folder(status_file_folder)

#Create status text file
set_hatch_status(STATUS_CLOSED, os.path.join(status_file_folder, status_file_name))

#!/usr/bin/env python

'''

!!!   MAKE SURE HATCH IS PHYSICALLY CLOSED WHEN STARTING UP RASPBERRY PI  !!!


'''

import os

status_file_folder = "/tmp/thecoop"
status_file_name = "hatch_status.txt"

STATUS_CLOSED = '0'
STATUS_OPEN = '1'
STATUS_IN_MOTION = '2'


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

print("Init package from __init__.py")

init_status_file_folder(status_file_folder)

#Create status text file
set_hatch_status(STATUS_CLOSED, os.path.join(status_file_folder, status_file_name))


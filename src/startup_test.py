print("Running python script on startup")

import os

file_folder = "/tmp/startuptest"


def init_folder(folder):
    
    print("Setting up startup test folder")
    # Create folder 
    if not os.path.exists(folder):
        os.mkdir(folder)
    
    
init_folder(file_folder)

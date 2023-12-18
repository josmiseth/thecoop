

from threading import Thread
from flask import Flask
import time

import sys
sys.path.append('/home/pi/projects/thecoop/')
from hatch_controller import start_controller

app = Flask(__name__)

# Run hatch_controller in background
def background_task():
        #while True:
        print("Run hatch controller in background")
        start_controller()
                #time.sleep(10)


@app.route('/')
def hello_world():
        return 'The hatch webapp test'

if __name__ == '__main__':
        
        # Start hatch controller in background
        background_thread = Thread(target=background_task)
        background_thread.start()

        app.run(debug=True, host='0.0.0.0', use_reloader=False)
#        app.run(debug=True, host='0.0.0.0')

        


from flask import Flask, render_template, url_for
from flask_responses import  json_response, xml_response, auto_response


import RPi.GPIO as GPIO      #Import GPIO library
import time                  #Import time library

GPIO.setmode(GPIO.BOARD)     #Use board pin numbering
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)     # Setup GPIO Pin 12 

app = Flask(__name__)

@app.route('/')
def index():
  
    input_state = GPIO.input(21) #Read and store value of input to a variable
    if input_state == False:     #Check whether pin is grounded
       print('Button Pressed')   #Print 'Button Pressed'
       time.sleep(0.5)           #Delay of 0.5s
       return  render_template ('index.html')
    

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0')
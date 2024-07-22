# import the libraries
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)                   

# set the pin numbers to be used from Broadcom chip

ledpin = 27 # assign a variable name to pin 4
pushpin = 16 # assign a variable name to pin 17
GPIO.setup(ledpin, GPIO.OUT) # set GPIO pin 4 as Output
GPIO.setup(pushpin, GPIO.IN) # set GPIO pin 17 as Input
GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW) # set the initial output of pin 4 to be LOW

while True:
           GPIO.output(ledpin, not GPIO.input(pushpin)) # read the inverse value of input pin 17
           sleep(0.2)

           

#Importing the Right libraries
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)     

ledpin = 27                                                
pushpin = 16                                       
GPIO.setup(ledpin, GPIO.OUT)          
GPIO.setup(pushpin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # using the internal Pull up resistor
GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)   

while True:
           GPIO.output(ledpin, not GPIO.input(pushpin))       # Reading the inverse value of input pin 17
           sleep(0.2)


           

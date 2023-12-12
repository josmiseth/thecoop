
# coding=utf-8

'''
Using a 10 kOhm pullup resitance

Wiring
Pullup resitance connected to 3V3 pin (3.3 V) (Black whire)
The other side of the switch (no resistance) connected to GPIO 23 (brown wire)



'''
 
 
import RPi.GPIO as GPIO
import datetime
import time


def my_callback(channel):

    if GPIO.input(channel) == GPIO.HIGH:
        print('\n▼  at ' + str(datetime.datetime.now()))
    else:
        print('\n ▲ at ' + str(datetime.datetime.now())) 
 
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.add_event_detect(23, GPIO.RISING, callback=my_callback)
 
    while True:
        time.sleep(10)
    #message = input('\nPress any key to exit.\n')
 
finally:
    GPIO.cleanup()
 
print("Goodbye!")
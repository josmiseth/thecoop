
# coding=utf-8

'''
Using a 10 kOhm pullup resitance

Wiring
Pullup resitance connected to 3V3 pin (3.3 V) (Black whire)
The other side of the switch (no resistance) connected to GPIO 18 (white wire)



'''
 
 
import RPi.GPIO as GPIO
import datetime
 
 
def is_lowtemp():
    state = False
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(22, GPIO.IN)
        state = GPIO.input(22)
    
 
    finally:
        GPIO.cleanup()
        
    return state
    
    
print(is_lowtemp())

 
'''
Demo code:

def my_callback(channel):
    if GPIO.input(channel) == GPIO.HIGH:
        print('\n▼  at ' + str(datetime.datetime.now()))
    else:
        print('\n ▲ at ' + str(datetime.datetime.now())) 
 
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN)
    GPIO.add_event_detect(18, GPIO.BOTH, callback=my_callback)
 
    message = input('\nPress any key to exit.\n')
 
finally:
    GPIO.cleanup()
 
print("Goodbye!")
'''

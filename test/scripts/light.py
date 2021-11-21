from signal import pause
from time import sleep
from gpiozero import PWMLED

led = PWMLED(24)

try:
    led.pulse()
    
except KeyboardInterrupt:
    pass

finally:
    led.close()
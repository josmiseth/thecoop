import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setwarnings(False)  # Disable warnings

# Define the pin for the LED
LED_PIN = 27

# Set up the LED pin as output
GPIO.setup(LED_PIN, GPIO.OUT)

print("Start flashing led")
try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED on
        time.sleep(1)  # Keep it on for 1 second
        GPIO.output(LED_PIN, GPIO.LOW)   # Turn LED off
        time.sleep(1)  # Keep it off for 1 second

except KeyboardInterrupt:
    print("Program interrupted by user.")

finally:
    GPIO.cleanup()  # Clean up GPIO settings on exit

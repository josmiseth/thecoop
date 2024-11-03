import RPi.GPIO as GPIO
import time

import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#print(GPIO.VERSION)
#GPIO.cleanup()  # Clean up any existing configurations before starting
import src

LED_PIN = src.PIN_RED_LED
BUTTON_PIN = src.PIN_PUSH_BUTTON

# Setup GPIO mode and warnings
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setwarnings(False)

# Setup LED pin as output and button pin as input with a pull-up resistor
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initial LED state
led_state = False

# Function to toggle LED
def toggle_led():
    global led_state
    led_state = not led_state  # Toggle LED state
    GPIO.output(LED_PIN, led_state)
    print("LED is ON" if led_state else "LED is OFF")

# Event handler function for button press
def button_pressed_callback(channel):
    # Remove event detection to prevent multiple triggers
    GPIO.remove_event_detect(BUTTON_PIN)

    # Toggle LED
    toggle_led()

    # Add a short delay for debounce
    time.sleep(0.2)

    # Re-enable event detection
    GPIO.add_event_detect(BUTTON_PIN, GPIO.BOTH, callback=button_pressed_callback, bouncetime=200)

# Add event detection on the button pin
GPIO.add_event_detect(BUTTON_PIN, GPIO.BOTH, callback=button_pressed_callback, bouncetime=200)

try:
    # Keep the program running
    print("Press the button to toggle the LED.")
    while True:
        time.sleep(1)  # Keep the program running to listen for events

except KeyboardInterrupt:
    print("Program terminated by user.")

finally:
    GPIO.cleanup()  # Cleanup all GPIO pins on exit

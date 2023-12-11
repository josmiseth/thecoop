# thecoop

This is a Raspberry Pi project for making a smart chicken coop. The first goal is to be able to open and close the hatch door in an automated way. This involves controlling an electric motor with four relays, and activate this based on the time of day and outside temperature. The hatch should go up in the mornig and close in the evening. However, when it is freezing cold outside, the hatch should stay closed. When the temperature increases to a set value, the hatch should open.

# GPIO pinout for Raspberry Pi 3 B+

![GPIO pinout](https://github.com/josmiseth/thecoop/blob/main/img/raspberry_pi_3b%2B_pins_2.jpeg "GPIO pinout")

![GPIO pinout](https://github.com/josmiseth/thecoop/blob/main/img/raspberry_pi_3b%2B_pins.jpeg "GPIO pinout")


# Relay setup

Test code: https://github.com/josmiseth/thecoop/blob/main/test/scripts/relay.py

![Setup for relay](https://github.com/josmiseth/thecoop/blob/main/img/relay_wiring_complete.jpeg "Relay wiring overview")


# Temperature sensor setup

https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/

# Diode setup

https://www.electronicwings.com/raspberry-pi/raspberry-pi-pwm-generation-using-python-and-c

Blinking: https://www.google.com/amp/s/www.teknotut.com/en/first-raspberry-pi-project-blink-led/amp/

Breathing diode: https://www.admfactory.com/breathing-light-led-on-raspberry-pi-using-python/

# Temperature relay setup

The hatch should not open if the outside temperature is lower than a specified temperature. This is controlled by an external unit where the user can set the limit temperature, and a relay is is set depending on if the outdoor temperature is higher or lower than this. There is also a buffer temperature difference to avoid that the relay switches multiple times when the temperature is oscillating at the limit. The Raspberry Pi needs to measure the state of the relay. This would be equivalent to reading the position of a switch.

https://projects.raspberrypi.org/en/projects/physical-computing/5

# Hall sensor

https://learn.sunfounder.com/lesson-1-hall-sensor/


# Mobile phone controller  

https://www.swift.org/getting-started/ https://www.swift.org/getting-started/


# Configure development environment 

Enable SSH on device: https://raspberrypi-guide.github.io/networking/connecting-via-ssh#:~:text=Enable%20SSH%20on%20the%20Raspberry%20Pi,-By%20default%2C%20SSH&text=To%20enable%20SSH%20via%20the,to%20SSH%20and%20click%20OK%20.

SSH setup for GitHub: https://www.google.com/amp/s/garywoodfine.com/setting-up-ssh-keys-for-github-access/%3Famp

Clone repo: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository

VScode: https://code.visualstudio.com/docs/setup/raspberry-pi


# Examples 

https://www.backyardchickens.com/articles/a-raspberry-pi-controlled-diy-coop-door-with-python-code.74113/

Used for thermostat 0/1 readout:
https://raspberrypi.stackexchange.com/questions/5083/read-input-from-the-gpio

Generally on pull-up resistors and switches:
https://grantwinney.com/using-pullup-and-pulldown-resistors-on-the-raspberry-pi/

Run program at startup:
https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/

Log run at startup:
https://en.wikipedia.org/wiki/Nohup

Crontab tips:
https://crontab.guru/every-1-minute


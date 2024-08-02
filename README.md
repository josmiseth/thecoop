# thecoop

This is a Raspberry Pi project for making a smart chicken coop. The first goal is to be able to open and close the hatch door in an automated way. This involves controlling an electric motor with four relays, and activate this based on the time of day and outside temperature. The hatch should go up in the morning and close in the evening. However, when it is freezing cold outside, the hatch should stay closed. When the temperature increases to a set value, the hatch should open.

![Exterior](https://github.com/josmiseth/thecoop/blob/main/img/Exterior.jpeg "Exterior")
![Inner workings](https://github.com/josmiseth/thecoop/blob/main/img/Setup.jpeg "Inner workings")

The system consists of
- A Raspberry Pi 3 connected via WiFi with a 5.1 V 3 A power supply 
- A quadruple relay to control the motor to move the hatch up and down
- A separate power 10-24 V power for the hatch motor
- A 18 V drill
- A temperature measurement unit with a relay which switches when the measured temperature is below a specified limit
- A push button unit with a pull-up resistor for controlling the hatch motor

The hatch of the chicken coop is set to open at a specified time (09:00) with cron schedule. However, if the temperature is lower than the specified temperature limit of the temperature measurement unit, the hatch will not open. A backup solution if the temperature measurement unit drops out for some reason is that Raspberry Pi calls the yr.no met API to check for the current temperature forecast, and checks if this is below a specified limit. The hatch opens one hour after sunset each day. The chickens have returned to the coop long before that.  The scheduling of this is handled through cron by sepeate jobs for each day of the year at specified times determined by the Suntime Python package. The hatch can be controlled via the push button as well. When the button is pushed, the door opens or closes independent of outdoor temperature. 

# Setup
Follow the following instructions to set up the system:
1. Download the newest Raspian 64 bit image to a SD card
1. Insert the SD card to the Raspberry Pi and startup
1. Run sudo apt-get update
1. Run sudo apt-get upgrade
1. Run ssh-keygen to create ssh keys
1. Add the public key to the Github repository https://github.com/settings/keys
1. Make a projects folder
1. Copy the clone ssh statement from Github: git@github.com:josmiseth/thecoop.git
1. Clone the respository on to the projects folder: git clone git@github.com:josmiseth/thecoop.git
1. Install emacs: sudo apt-get install emacs
1. Install Apscheduler (for all users including admin) with: sudo apt install python3-apscheduler
1. Install Suntime with: sudo apt install python3-suntime
1. Run: python3 ~/projects/thecoop/src/hatch_controller.py
1. Log on a terminal via ssh
1. Run: nohup python3 ~/projects/thecoop/src/hatch_controller.py &
1. Terminate terminal, and the process will continue to run.

# Launch on reboot

Use the following setup to launch from reboot. It should be mentioned that with the current setup, this requires that the hatch is in position down when the Raspberry Pi is rebooted, for instance after an electriciy outage. However, as I am using a modified battery power drill with a torque limiter. If the hatch is in an open position when the Pi reboots and the hatch is commanded to open, the hatch is physicall stopped to not move furthern up than the open position, and the torque limiter will make the power drill run as long as it is set to run. This syncronises the open status in the status file with the actual status of the hatch. If such the hatch would not be set up like this, a limit switch could be added to measure the physical status of the hatch upon reboot, and a syncronization of the digital status and the physical status could be ensured.

1. Go to the bin folder cd ~/projects/thecoop/bin
1. Make the launcher.sh scrip executable with the command: chmod 755 launcher.sh
1. Make a folder called ~/projects/thecoop/logs
1. Change the crontab by typing: sudo crontab -e
1. Select your favorite text editor if this is prompted for
1. At the bottom of the crontab file enter the line: @reboot sleep 60 && sh /home/pi/thecoop/bin/launcher.sh >/home/pi/thecoop/logs/cronlog 2>&1
1. Make sure that that the paths in the crontab file line are corresponding to the ones you have on your Pi
1. Save the crontab file

You can test this by typing "sudo reboot" and wait for the reboot (and for the 60 second sleep). Check that the cronlog file is in the logs directory by typing "cat cronlog".


Got inspiration from: https://www.instructables.com/Raspberry-Pi-Launch-Python-script-on-startup/

# GPIO pinout for Raspberry Pi 3 B+

![GPIO pinout](https://github.com/josmiseth/thecoop/blob/main/img/raspberry_pi_3b%2B_pins_2.jpeg "GPIO pinout")

![GPIO pinout](https://github.com/josmiseth/thecoop/blob/main/img/raspberry_pi_3b%2B_pins.jpeg "GPIO pinout")

Relay wiring

|Relay channel  |   Wire color  |   Port  |   Function
|---------------|---------------|------------|-------------------
|    4          |   Yellow      |   GPIO17   |   Minus wire hatch up
|    3          |   Green       |   GPIO05   |   Plus wire hatch up
|    2          |   Dark blue   |   GPIO06   |   Plus wire hatch down
|    1          |   Pink        |   GPIO21   |   Minus wire hatch down

Push button wiring
|Wire color    |    Port
|--------------|------------------
|Black         |    3.3 V (pin 1)
|White         |    GPIO23


Temperature relay wiring
|Wire color   | Port
|-------------|---------
|Brown        | GPIO22


Ultrasound distance sensor
|Gate         |Wire color   | Port
|-------------|-------------|---------
|Echo         |White        | GPIO24
|Trig	      |Purple	    | GPIO04
|Alarm (LED)  |Brown	    | GIPO27
|Ground       |Black        | GND
|Vcc          |Red          | 5V

Ultrasound sensor setup:
![Ultrasound sensor setup](https://github.com/josmiseth/thecoop/blob/main/img/IMG_2891.jpeg "Setuo")



# Relay setup

Test code: https://github.com/josmiseth/thecoop/blob/main/test/scripts/relay.py

![Setup for relay](https://github.com/josmiseth/thecoop/blob/main/img/relay_wiring_complete.jpeg "Relay wiring overview")

# Webserver and water level measurement

https://helloworld.co.in/article/smart-water-tank

Install Ubuntu through an USB memory stick: 
https://gcore.com/learning/how-to-install-ubuntu-on-windows/
using UNetBootin: https://unetbootin.github.io/

Follow instructions to set up the webserver and mySQL
 
Start the Xampp panel with: sudo /opt/lampp/manager-linux-x64.run


Install code on Raspberry Pi

# Temperature sensor setup

https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/

# Diode setup

https://www.electronicwings.com/raspberry-pi/raspberry-pi-pwm-generation-using-python-and-c

Blinking: https://www.google.com/amp/s/www.teknotut.com/en/first-raspberry-pi-project-blink-led/amp/

Breathing diode: https://www.admfactory.com/breathing-light-led-on-raspberry-pi-using-python/

# Temperature relay setup

The hatch should not open if the outside temperature is lower than a specified temperature. This is controlled by an external unit where the user can set the limit temperature, and a relay is is set depending on if the outdoor temperature is higher or lower than this. There is also a buffer temperature difference to avoid that the relay switches multiple times when the temperature is oscillating at the limit. The Raspberry Pi needs to measure the state of the relay. This would be equivalent to reading the position of a switch.

https://projects.raspberrypi.org/en/projects/physical-computing/5

https://raspberrypi.stackexchange.com/questions/5083/read-input-from-the-gpio

https://grantwinney.com/using-pullup-and-pulldown-resistors-on-the-raspberry-pi/
        

# Ultrasound sensor for water level measurement

https://helloworld.co.in/article/smart-water-tank

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

APScheduler and crontab example:
https://www.javatpoint.com/apschedular-python-example

Crontab tips:
https://crontab.guru/every-1-minute

Locationforecast API:
https://api.met.no/weatherapi/locationforecast/2.0/documentation

Connection with Futurehome over MQTT:
https://support.futurehome.no/hc/en-no/articles/360033256491-Local-API-access-over-MQTT-Beta-

How to use the Paho Python MQTT client:
http://www.steves-internet-guide.com/into-mqtt-python-client/


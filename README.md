# thecoop

This is a Raspberry Pi project for making a smart chicken coop. The first goal is to be able to open and close the hatch door in an automated way. This involves controlling an electric motor with four relays, and activate this based on the time of day and outside temperature. The hatch should go up in the mornig and close in the evening. However, when it is freezing cold outside, the hatch should stay closed. When the temperature increases to a set value, the hatch should open.

# GPIO pinout for Raspberry Pi 3 B+

![GPIO pinout](https://github.com/josmiseth/thecoop/blob/main/img/raspberry_pi_3b%2B_pins.jpeg "GPIO pinout")


# Relay setup

![Setup for relay](https://github.com/josmiseth/thecoop/blob/main/img/relay_wiring_overview.jpeg "Relay wiring overview")

![Relay wiring details](https://github.com/josmiseth/thecoop/blob/main/img/relay_wiring.jpeg "Relay wiring details")




SSH setup: https://www.google.com/amp/s/garywoodfine.com/setting-up-ssh-keys-for-github-access/%3Famp

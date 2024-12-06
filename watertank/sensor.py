
#Project: Smart Water Tank
#Created by: Jitesh Saini
#Modified by: Jo Smiseth

# Code for the HCSR-04 ultrasound sensor

#you can use the setup_cron.sh bash script to install a cron job to automatically execute this file every minute.
import pigpio
import time
import os
import datetime

# GPIO pin definitions
TRIG = 4
ECHO = 24
ALARM = 27

# Initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    exit("Failed to connect to pigpio daemon.")

# Set up GPIO pins
pi.set_mode(TRIG, pigpio.OUTPUT)
pi.set_mode(ECHO, pigpio.INPUT)
pi.set_mode(ALARM, pigpio.OUTPUT)

# Ensure initial states
pi.write(TRIG, 0)
pi.write(ALARM, 0)

print("Waiting for sensor to settle")
time.sleep(1)  # Settling time

def get_distance():
    dist_add = 0
    start_function = time.time()
    for x in range(20):
        try:
            # Trigger pulse
            pi.write(TRIG, 1)
            time.sleep(0.00001)
            pi.write(TRIG, 0)
            print("Sent trigger pulse")
            # Measure pulse duration
            while pi.read(ECHO) == 0:
                pulse_start = time.time()
                #print(pi.read(ECHO))
                if time.time() - start_function > 10:
                    raise Exception("No response from ultrasound unit")

            while pi.read(ECHO) == 1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            dist_add += distance
            print(x, "distance:", round(distance, 3))
            time.sleep(0.1)  # 100ms interval between readings
         
        except Exception as e:
            raise Exception(e)

    avg_dist = dist_add / 20
    return round(avg_dist, 3)

def send_data_to_remote_server(dist):
    url_remote = f"http://10.0.0.54:80/the-coop-page/insert_data.php?dist={dist}"
    cmd = f"curl -s {url_remote}"
    os.system(cmd)
    print(cmd)

def low_level_warning(dist):
    tank_height = 114  # Set your tank height here
    level = tank_height - dist
    if level < 40:
        print("Level low:", level)
        for _ in range(20):
            pi.write(ALARM, 1)
            time.sleep(1)
            pi.write(ALARM, 0)
            time.sleep(1)
    else:
        print("Level OK")

def main():
    try:
        distance = get_distance()
        print("Distance:", distance)
        send_data_to_remote_server(distance)
        low_level_warning(distance)
        print("---------------------")
    except Exception as e:
        print(f"Measurement failed with exception: {e}")
    finally:
        pi.stop()  # Close pigpio connection

if __name__ == '__main__':
    main()


#Project: Smart Water Tank
#Created by: Jitesh Saini
#Modified by: Jo Smiseth

#you can use the setup_cron.sh bash script to install a cron job to automatically execute this file every minute.

import RPi.GPIO as GPIO
import time,os

import datetime
from gpiozero import Buzzer

TRIG = 4
ECHO = 24
ALARM = 27

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)

GPIO.setup(ALARM,GPIO.OUT)
GPIO.output(ALARM, False)
#buzzer = Buzzer(ALARM)

print ("Waiting For Sensor To Settle")
time.sleep(1) #settling time 
print("test1")
def get_distance():
   dist_add = 0

   for x in range(20):
      try:
         GPIO.output(TRIG, True)
         time.sleep(0.00001)
         GPIO.output(TRIG, False)
         while GPIO.input(ECHO)==0:
                 pulse_start = time.time()
         while GPIO.input(ECHO)==1:
                 pulse_end = time.time()

         pulse_duration = pulse_end - pulse_start
         distance = pulse_duration * 17150
         distance = round(distance, 3)
         print (x, "distance: ", distance)
         dist_add = dist_add + distance
         #print "dist_add: ", dist_add
         time.sleep(.1) # 100ms interval between readings
         
      except Exception as e: 
		
         pass

   avg_dist=dist_add/20
   dist=round(avg_dist,3)


   #print ("dist: ", dist)
   return dist

   

def sendData_to_remoteServer(dist):
	#replace 192.168.1.2 with the IP address of your webserver
	url_remote="http://10.0.0.54:8080/water-tank/insert_data.php?dist=" + str(dist)
	cmd="curl -s " + url_remote
	result=os.popen(cmd).read()
	print (cmd)
	
		
	
def low_level_warning(dist):
	tank_height=114 #set your tank height here
	level=tank_height-dist
	if(level<40):
               print("level low : ", level)
               #Tibber pushnotification
               #mutation{sendPushNotification(input: {title: "hei", message: "testing", screenToOpen:NOTIFICATIONS})}

               for n in range(0,20):
                      GPIO.output(ALARM, True)
                      time.sleep(1)
                      GPIO.output(ALARM, False)
                      time.sleep(1)                      
	else:
		print("level ok")



                

def main():
	
	distance=get_distance()
	
	print ("distance: ", distance)
	sendData_to_remoteServer(distance)
	low_level_warning(distance)
	print ("---------------------")
	
	
if __name__ == '__main__':
    main()


#!/usr/bin/python3

import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)

def on_log(client, userdata, level, buf):
    print("log: " + buf)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection. Returned code=", rc)
        

client = mqtt.Client("The coop")

client.on_message=on_message
client.on_log = on_log
client.on_connect = on_connect

client.username_pw_set("","")
client.connect("10.0.0.60",port=1884, keepalive=60, bind_address="")

client.loop_start()
client.subscribe("pt:j1/#")

#client.subscribe("pt:j1/mt:evt/rt:ad/rn:zigbee/ad:1")

#Outdoor thermometer:
client.subscribe("pt:j1/mt:evt/rt:dev/rn:zigbee/ad:1/sv:sensor_temp/ad:5_1")

while True:
    time.sleep(10)
#time.sleep(10)

client.loop_stop()

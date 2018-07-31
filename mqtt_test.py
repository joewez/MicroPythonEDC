import network
import time
import machine
import gc
from umqtt.simple import MQTTClient
from shields import ds18b20_shield

#
# connect ESP8266 to Adafruit IO using MQTT
#
myMqttClient = "joew-mqtt-client"  # can be anything unique
adafruitIoUrl = "io.adafruit.com" 
adafruitUsername = "bitninja"  # can be found at "My Account" at adafruit.com
adafruitAioKey = "d271a68e416348fab5aa06df941a560e"  # can be found by clicking on "VIEW AIO KEYS" when viewing an Adafruit IO Feed
c = MQTTClient(myMqttClient, adafruitIoUrl, 0, adafruitUsername, adafruitAioKey)
c.connect()

shield = ds18b20_shield.DS18B20_Shield()

initialized = False

while True:
    tempInDegF = shield.farenheit() - 15.0

    if not initialized and tempInDegF > 100.0:
        initialized = True
    else:
        c.publish("bitninja/feeds/ITRoomTempInDegF", str(tempInDegF))  # publish temperature to adafruit IO feed
        print(tempInDegF)

    time.sleep(60)  # number of seconds between each Publish
  
    gc.collect()

c.disconnect()
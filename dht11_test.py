import time
from shields import dht11_shield

# create object to retrieve the temp
dht_shield = dht11_shield.DHT11_Shield()

# infinite loop
while True:

    tempC, tempF, humidity = dht_shield.read_data()

    #offset
    tempF -= 5.0

    print('Temp:{0} F Humidity:{1}%'.format(tempF, humidity))

    # wait for the next check
    time.sleep_ms(2000)
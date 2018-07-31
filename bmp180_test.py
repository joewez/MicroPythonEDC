# basic test for the BMP180 shield

import time
from shields import bmp180_shield

# create object to retrieve the temp
bmp = bmp180_shield.BMP180_Shield()

# infinite loop
while True:

    alt = bmp.altitude()
    pre = bmp.pressure()
    temp = bmp.farenheit()
    print('Altitude: {0}(m)  Pressure: {1}(pa) Temperature: {2}'.format(alt, pre, temp))

    #print(bmp.bmp.compvaldump())
    # wait for the next check
    time.sleep_ms(2000)

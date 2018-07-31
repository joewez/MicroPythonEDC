# altitude sensor and output
# uses the bmp180 and the small OLED shields
# author: Joseph G. Wezensky

import time
from shields import bmp180_shield
from drivers import oled

# create object to retrieve the temp
bmp = bmp180_shield.BMP180_Shield()

# create object to work with display
oled = oled.OLED(4, 5, 64, 48)

# infinite loop
while True:

    alt = bmp.altitude()
    pre = bmp.pressure()
    tmp = bmp.farenheit()

    oled.clear()
    oled.smalltext("{0:5.2f} m".format(alt))
    oled.smalltext("{0} pa".format(pre),x=0,y=8)
    oled.smalltext("{0:5.2f} F".format(tmp),x=0,y=16)
    oled.show()

    # wait for the next check
    time.sleep_ms(2000)

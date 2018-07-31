import time
from drivers import oled
from shields import datalogger_shield
from shields import dht11_shield

dht_shield = dht11_shield.DHT11_Shield()

datalogger = datalogger_shield.DataLogger_Shield()

display = oled.OLED(14, 12, 128, 64)

def gfxfile(num):
    return '/graphics/num{:d}.txt'.format(num)

while True:

    display.clear()

    temp = dht_shield.farenheit()
    temp -= 5.0
    humidity = dht_shield.humidity()

    display.smalltext("temp:", 5, 5)
    display.text("{:d}".format(round(temp)), 25, 3)
    display.smalltext("humidity:", 50, 5)
    display.text("{:d}%".format(round(humidity)), 90, 3)

    hour = datalogger.hour()

    suffix = '/graphics/am.txt'
    if hour >= 12:
        suffix = '/graphics/pm.txt'    

    top = 26

    if hour > 12:
        hour -= 12
    if hour > 9:
        display.graphic(gfxfile(1), 5, top)
        display.graphic(gfxfile(hour - 10), 25, top)
    elif hour > 0:
        display.graphic(gfxfile(hour), 25, top)
    else:
        display.graphic(gfxfile(1), 5, top)
        display.graphic(gfxfile(2), 25, top)

    display.graphic('/graphics/numcolon.txt', 47, top)

    minute = datalogger.minute()
    min1, min2 = divmod(minute, 10)
    display.graphic(gfxfile(min1), 60, top)
    display.graphic(gfxfile(min2), 80, top)

    display.graphic(suffix, 100, 38)

    display.show()

    time.sleep_ms(300)
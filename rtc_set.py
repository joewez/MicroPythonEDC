from drivers import ds1307
from machine import I2C, Pin

i2c = I2C(sda=Pin(4), scl=Pin(5))

rtc = ds1307.DS1307(i2c)

datetime = ds1307.datetime_tuple(year=2017, month=9, day=12, weekday=2, hour=19, minute=43)

rtc.datetime(datetime)

print(rtc.datetime())

from drivers import ds1307
from machine import I2C, Pin, RTC
from ntptime import settime
import utime

def syncOnboardFromNTP():
    settime()

def syncOnboardFromExternal():
    i2c = I2C(sda=Pin(4), scl=Pin(5))
    external_rtc = ds1307.DS1307(i2c)
    (year, month, day, weekday, hour, minute, second, millisecond) = external_rtc.datetime()
    
    onboard_rtc = RTC()
    onboard_rtc.datetime((year, month, day, weekday, hour, minute, second, 0))

def syncExternalFromNTP():
    settime()

    onboard_rtc = RTC()
    (year, month, day, weekday, hour, minute, second, millisecond) = onboard_rtc.datetime()

    i2c = I2C(sda=Pin(4), scl=Pin(5))
    external_rtc = ds1307.DS1307(i2c)
    newtime = ds1307.datetime_tuple(year=year, month=month, day=day, weekday=weekday, hour=hour, minute=minute)
    external_rtc.datetime(newtime)

def localTime(offset=-5):
    newtime = utime.time() + (60*60)*offset
    (year, month, mday, hour, minute, second, weekday, yearday)=utime.localtime(newtime)
    print('{0}-{1:02}-{2:02} {3:02}:{4:02}'.format(year, month, mday, hour, minute))


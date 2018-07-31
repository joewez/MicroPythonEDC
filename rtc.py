from drivers import ds1307
from machine import I2C, Pin, RTC
from ntptime import settime
import utime

def SyncFromNTP():
    settime()

def SyncFromExternal():
    i2c = I2C(sda=Pin(4), scl=Pin(5))
    external_rtc = ds1307.DS1307(i2c)
    (year, month, day, weekday, hour, minute, second, millisecond) = external_rtc.datetime()
    
    onboard_rtc = RTC()
    onboard_rtc.datetime((year, month, day, weekday, hour, minute, second, 0))

#def syncExternalFromNTP():
#    settime()

#    onboard_rtc = RTC()
#    (year, month, day, weekday, hour, minute, second, millisecond) = onboard_rtc.datetime()

#    i2c = I2C(sda=Pin(4), scl=Pin(5))
#    external_rtc = ds1307.DS1307(i2c)
#    newtime = ds1307.datetime_tuple(year=year, month=month, day=day, weekday=weekday, hour=hour, minute=minute)
#    external_rtc.datetime(newtime)

def LocalTime(offset=-5, pretty=False):
    newtime = utime.time() + (60*60)*offset
    (year, month, mday, hour, minute, second, weekday, yearday)=utime.localtime(newtime)
    if pretty:
        timestr = '{0}-{1:02}-{2:02} {3}'.format(year, month, mday, PrettyTime(hour, minute))
    else:
        timestr = '{0}-{1:02}-{2:02} {3:02}:{4:02}'.format(year, month, mday, hour, minute)
    return timestr

def PrettyTime(hour, minute):
    timestr = ''
    if hour > 12:
        timestr = str(hour - 12)
    elif hour == 0:
        timestr = '12'
    else:
        timestr = str(hour)
    timestr += ':{0:02}'.format(minute)
    timestr += ' am' if hour <= 11 else ' pm'
    return timestr

#def test():
#    print(PrettyTime(6,54))
#    print(PrettyTime(13,13))
#    print(PrettyTime(0,27))
#    print(PrettyTime(23,54))

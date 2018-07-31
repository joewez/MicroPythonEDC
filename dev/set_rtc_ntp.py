from drivers import ds1307
from machine import I2C, Pin, RTC
from ntptime import settime
import utime

#set the onboard RTC
x = settime()

def pp(dt):
    return '{0}-{1:02}-{2:02} {3:02}:{4:02}'.format(dt[0], dt[1], dt[2], dt[4], dt[5])

def pt(dt):
    return '{0}-{1:02}-{2:02} {3:02}:{4:02}'.format(dt[0], dt[1], dt[2], dt[3], dt[4])

# print the times they provide
rtc = RTC()
gmttime = rtc.datetime()
print('gmt time:{0}'.format(pt(gmttime)))
localtime = utime.localtime()
print('local time:{0}'.format(pt(localtime)))

# set the external RTC
i2c = I2C(sda=Pin(4), scl=Pin(5))
external_rtc = ds1307.DS1307(i2c)
#newtime = ds1307.datetime_tuple(year=gmttime[0], month=gmttime[1], day=gmttime[2], weekday=gmttime[6], hour=gmttime[3], minute=gmttime[4])
newtime = ds1307.datetime_tuple(year=localtime[0], month=localtime[1], day=localtime[2], weekday=localtime[6], hour=localtime[3], minute=localtime[4])
external_rtc.datetime(newtime)
newtimeout = pp(newtime)

print('external RTC time:{0}'.format(newtimeout))

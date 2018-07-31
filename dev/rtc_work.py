from drivers import ds1307
from machine import I2C, Pin, RTC
import utime

def syncRTC():
    from ntptime import settime
    x = settime()
    return x

def localTime(offset=-5):
    newtime = utime.time() + (60*60)*offset
    (year, month, mday, hour, minute, second, weekday, yearday)=utime.localtime(newtime)
    print('{0}-{1:02}-{2:02} {3:02}:{4:02}'.format(year, month, mday, hour, minute))

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

print('---------------------------------')

# for time convert to second
# for gmt. For me gmt-5. 
offset = -5 
time2 = utime.time() + (60*60)*offset

# for second to convert time
(_year, _month, _mday, _hour, _minute, _second, _weekday, _yearday)=utime.localtime(time2)

dt = (_year, _month, _mday, _hour, _minute, _second, _weekday, _yearday)
print(pt(dt))
# first 0 = week of year
# second 0 = milisecond
#rtc.datetime((_year, _month, _mday, 0, _hour, _minute, _second, 0))

newtime = ds1307.datetime_tuple(year=_year, month=_month, day=_mday, weekday=_weekday, hour=_hour, minute=_minute)
external_rtc.datetime(newtime)
newtimeout = pp(newtime)

print('external RTC time:{0}'.format(newtimeout))

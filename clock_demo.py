import time
from drivers import oled
from shields import rtc_shield

rtc = rtc_shield.RTC_Shield()

display = oled.OLED(4, 5, 64, 48)

while True:

    display.clear()
    hour = rtc.hour()
    minute = rtc.minute()
    timestr = pretty_time(hour, minute)
    print(timestr)
    display.text(timestr)
    display.show()
    
    time.sleep(30)

from drivers import max7219d
from machine import Pin, SPI
from ntptime import settime
from machine import RTC
import time

#Wemos D1 Mini   max7219 8x8 LED Matrix
#    5V          VCC
#    GND         GND
#    D7 MOSI     DIN
#    D8          CS
#    D5 SCK      CLK

spi = SPI(1, baudrate=10000000, polarity=0, phase=0)
display = max7219d.Max7219D(spi, Pin(15))

display.scan(8)
display.decode(255)

count = 180
settime()

rtc = RTC()

for i in range(8):
    display.digit(i, 15)


while True:
    dt = rtc.datetime()
    mon = dt[1]
    day = dt[2]
    hour = dt[4] - 5
    min = dt[5]

    mon_digit1 = mon // 10
    mon_digit2 = mon % 10
    if mon_digit1 == 0:
        display.digit(0, 15)
    else:
        display.digit(0, mon_digit1)
    display.digit(1, mon_digit2)

    day_digit1 = day // 10
    day_digit2 = day % 10
    if day_digit1 == 0:
        display.digit(2, 15)
    else:
        display.digit(2, day_digit1)
    if day_digit2 == 0:
        display.digit(3, 15)
    else:
        display.digit(3, day_digit2)

    hour_digit1 = hour // 10
    hour_digit2 = hour % 10
    if hour_digit1 == 0:
        display.digit(4, 15)
    else:
        display.digit(4, hour_digit1)
    display.digit(5, hour_digit2)

    min_digit1 = min // 10
    display.digit(6, min_digit1)
    min_digit2 = min % 10
    display.digit(7, min_digit2)

    time.sleep(10)

    count -= 1
    if count <= 0:
        settime()
        count = 180
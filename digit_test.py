from drivers import max7219d
from machine import Pin, SPI

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

display.digit(0, 0)
display.digit(1, 1)
display.digit(2, 2)
display.digit(3, 3)

display.digit(4, 4)
display.digit(5, 5)
display.digit(6, 6)
display.digit(7, 7)

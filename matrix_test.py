from drivers import max7219m
from machine import Pin, SPI

#Wemos D1 Mini   max7219 8x8 LED Matrix
#    5V          VCC
#    GND         GND
#    D7 MOSI     DIN
#    D8          CS
#    D5 SCK      CLK

spi = SPI(1, baudrate=10000000, polarity=0, phase=0)
display = max7219m.Max7219M(spi, Pin(15), 4)
display.brightness(0)
display.fill(0)
display.text('1234',0,0,1)
display.show()

display.fill(0)
display.show()

display.pixel(0,0,1)
display.pixel(1,1,1)
display.hline(0,4,8,1)
display.vline(4,0,8,1)
display.line(8, 0, 16, 8, 1)
display.rect(17,1,6,6,1)
display.fill_rect(25,1,6,6,1)
display.show()

display.fill(0)
display.text('dead',0,0,1)
display.text('beef',32,0,1)
display.show()

display.fill(0)
display.text('12345678',0,0,1)
display.show()
display.scroll(-8,0) # 23456788
display.scroll(-8,0) # 34567888
display.show()
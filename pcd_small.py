from drivers import pcd8544
from machine import Pin, SPI
import time
from drivers import font454

spi = SPI(1, baudrate=4000000, polarity=0, phase=0)
#spi.init(baudrate=8000000, polarity=0, phase=0)
cs = Pin(2)
dc = Pin(15)
rst = Pin(0)

# backlight on
bl = Pin(5, Pin.OUT, value=1)

lcd = pcd8544.PCD8544(spi, cs, dc, rst)

#lcd.reset()
#lcd.init()

# use the framebuf
import framebuf
buffer = bytearray((lcd.height // 8) * lcd.width)
framebuf = framebuf.FrameBuffer1(buffer, lcd.width, lcd.height)

text = """\
MicroPython is a lean
and efficient impleme
ntation of the Python
3 programming languag
e that includes a sma
ll subset of the Pytho
n standard library
"""

font454.text(framebuf, text, 0, 0)
lcd.position(0, 0)
lcd.data(buffer)


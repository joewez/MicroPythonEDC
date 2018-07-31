from drivers import tm1640
from machine import Pin
import framebuf

class TM1640_Shield:

    def __init__(self):
        self.tm = tm1640.TM1640(clk=Pin(14), dio=Pin(13))
        self.tm.brightness(7)
        self.buf = bytearray(8)
        self.fb = framebuf.FrameBuffer(self.buf, 8, 8, framebuf.MONO_HMSB)

    def clear(self):
        self.fb.fill(0)

    def pixel(self, x, y, c):
        self.fb.pixel(x, y, c)

    def show(self):
        self.tm.write_hmsb(self.buf)
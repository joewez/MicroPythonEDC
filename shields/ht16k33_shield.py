from machine import I2C, Pin
from drivers import ht16k33

class HT16K33_Shield:

    def __init__(self):
        i2c = I2C(sda=Pin(4), scl=Pin(5))
        self.matrix = ht16k33.Matrix8x8(i2c)
        self.matrix.brightness(15)
        self.matrix.blink_rate(0)

    def clear(self):
        self.matrix.fill(0)

    def fill(self, color):
        self.matrix.fill(color)

    def pixel(self, x, y, color=1):
        self.matrix.pixel(x, y, color)

    def show(self):
        self.matrix.show()
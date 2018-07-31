# bmp180_shield.py
# Class model wrapper for the Wemos D1 Mini BMP180 shield
# Author: JGWezensky (joewez@gmail.com)
# License: MIT License (https://opensource.org/licenses/MIT)

import machine
from machine import I2C, Pin
from drivers import bmp180

class BMP180_Shield:

    def __init__(self):
        i2c = I2C(sda=Pin(4), scl=Pin(5), freq=100000)
        self.bmp = bmp180.BMP180(i2c)
        self.bmp.oversample_set = 2
        self.bmp.baseline = 101325

    def temperature(self):
        return self.bmp.temperature

    def pressure(self):
        return self.bmp.pressure

    def altitude(self):
        return self.bmp.altitude

    def celsius(self):
        return self.bmp.temperature

    def farenheit(self):
        return (self.celsius() * 1.8) + 32.0
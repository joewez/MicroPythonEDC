from machine import Pin,I2C

i2c = I2C(sda=Pin(5), scl=Pin(4))

i2c.scan()

from drivers import hmc5883l

m = hmc5883l.HMC5883L(i2c)

import time
while True:
    print(m.heading())
    time.sleep(0.5)
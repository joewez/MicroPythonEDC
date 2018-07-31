from machine import I2C
import math
from array import array

class HMC5883L():
    
    __scales = {
        "0.88": [0, 0.73],
        "1.3": [1, 0.92],
        "1.9": [2, 1.22],
        "2.5": [3, 1.52],
        "4.0": [4, 2.27],
        "4.7": [5, 2.56],
        "5.6": [6, 3.03],
        "8.1": [7, 4.35]}
        
    def __init__(self, i2c, address=30, gauss="1.3", declination=(0,0)):
        self.bus = i2c
        self.address = address
        degrees, minutes = declination
        self.__declDegrees = degrees
        self.__declMinutes = minutes
        self.__declination = (degrees + minutes / 60) * math.pi / 180
        reg, self.__scale = self.__scales[gauss]
        self.bus.writeto_mem(self.address, 0x00, bytearray([0x70])) # 8 Average, 15 Hz, normal measurement 
        self.bus.writeto_mem(self.address, 0x01, bytearray([reg << 5])) # Scale 
        self.bus.writeto_mem(self.address, 0x02, bytearray([0x00])) # Continuous measurement 
    
    def declination(self):
        return (self.__declDegrees, self.__declMinutes)
    
    def bytes_toint(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def twos_complement(self, val, len): # Convert two's complement to integer
        if (val & (1 << len - 1)):
            val = val - (1<<len)
        return val

    def __convert(self, data, offset):
        x = data[offset] << 8
        #print(x)
        y = data[offset + 1]
        #print(y)
        z = x | y
        #print(z)
        #val = self.twos_complement(z, 16)
        val = self.bytes_toint(data[offset], data[offset + 1])
        if val == -4096: 
            #print(val)
            return None
        return round(val * self.__scale, 4)

    def axes(self):
        #data = array('B', [0]*6)
        data = self.bus.readfrom_mem(self.address, 0x03, 6) #Reading just the necessary registers instead of the whole memory as it was in rm-hull's version
        #print(data)
        x = self.__convert(data, 0)
        y = self.__convert(data, 4)
        z = self.__convert(data, 2)
        #print(x, y, z)
        return (x,y,z)

    def heading(self):
        (x, y, z) = self.axes()
        headingRad = math.atan2(y, x)
        headingRad += self.__declination
        # Correct for reversed heading
        if headingRad < 0:
            headingRad += 2 * math.pi
        # Check for wrap and compensate
        elif headingRad > 2 * math.pi:
            headingRad -= 2 * math.pi
        # Convert to degrees from radians
        headingDeg = headingRad * 180 / math.pi
        return headingDeg

    def degrees(self, headingDeg):
        degrees = math.floor(headingDeg)
        minutes = round((headingDeg - degrees) * 60)
        return (degrees, minutes)

    def __str__(self):
        (x, y, z) = self.axes()
        return "Axis X: " + str(x) + " " \
               "Axis Y: " + str(y) + " " \
               "Axis Z: " + str(z) + " " \
               "Heading: " + str(self.heading()) + "\n"

#"Declination: " + self.degrees(self.declination()) + "\n" \ #It gives an error on MicroPython and I've yet to see how it's supposed to work at all

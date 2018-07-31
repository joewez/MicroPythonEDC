import machine
import neopixel
import time

class Neo7_Shield():

    def __init__(self):
        pin = machine.Pin(4, machine.Pin.OUT)
        self.count = 7
        self.np = neopixel.NeoPixel(pin, self.count)

    def off(self):
        for i in range(self.count):
            self.np[i] = (0, 0, 0)
        self.np.write()

    def color(self, red, green, blue):
        for i in range(self.count):
            self.np[i] = (red, green, blue)
        self.np.write()

    def red(self, intensity=255):
        for i in range(self.count):
            self.np[i] = (intensity, 0, 0)
        self.np.write()

    def green(self, intensity=255):
        for i in range(self.count):
            self.np[i] = (0, intensity, 0)
        self.np.write()

    def blue(self, intensity=255):
        for i in range(self.count):
            self.np[i] = (0, 0, intensity)
        self.np.write()

    def white(self, intensity=255):
        for i in range(self.count):
            self.np[i] = (intensity, intensity, intensity)
        self.np.write()

    def wheel(self, pos):
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)

    def rainbow(self):
        for i in range(self.count):
            self.np[i] = self.wheel((int(i * 256 / self.count)) & 255)
        self.np.write()

    def rainbow_cycle(self, delay=50):
        for j in range(256):            
            for i in range(self.count):
                self.np[i] = self.wheel(j & 255)
            self.np.write()
            time.sleep_ms(delay)

    def rainbow_animate(self, cycles=1, delay=50):
        if cycles == 0:
            while True:
                self.rainbow_cycle(delay)
        else:
            for i in range(cycles):
                self.rainbow_cycle(delay)

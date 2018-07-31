import machine
import neopixel
import time

class WS2812B_Shield():

    def __init__(self):
        pin = machine.Pin(4, machine.Pin.OUT)
        self.np = neopixel.NeoPixel(pin, 1)

    def off(self):
        self.np[0] = (0, 0, 0)
        self.np.write()

    def color(self, red, green, blue):
        self.np[0] = (red, green, blue)
        self.np.write()

    def red(self, intensity=255):
        self.np[0] = (intensity, 0, 0)
        self.np.write()

    def green(self, intensity=255):
        self.np[0] = (0, intensity, 0)
        self.np.write()

    def blue(self, intensity=255):
        self.np[0] = (0, 0, intensity)
        self.np.write()

    def white(self, intensity=255):
        self.np[0] = (intensity, intensity, intensity)
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

    def rainbow_cycle(self, delay=50):
        for j in range(256):            
            self.np[0] = self.wheel(j & 255)
            self.np.write()
            time.sleep_ms(delay)

    def rainbow(self, cycles=1, delay=50):
        if cycles == 0:
            while True:
                self.rainbow_cycle(delay)
        else:
            for i in range(cycles):
                self.rainbow_cycle(delay)

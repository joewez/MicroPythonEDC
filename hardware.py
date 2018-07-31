import machine
from machine import I2C, Pin
import ssd1306
import neopixel
import time

class Hardware:

    # Constructor initializes all the hardware objects

    def __init__(self):
        self.i2c = I2C(sda=Pin(0), scl=Pin(2))
        self.display = ssd1306.SSD1306_I2C(128, 64, self.i2c, 0x3c, False)
        self.np = neopixel.NeoPixel(machine.Pin(4), 1)
        self.button1 = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
        self.button2 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
        self.button3 = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
        self.buzzer = machine.PWM(machine.Pin(5))

    # OLED display routines

    def oled_clear(self):
        self.display.fill(0)

    def oled_pixel(self, x, y, col):
        self.display.pixel(x, y, col)

    def oled_show(self):
        self.display.show()

    def oled_text(self, text, x = 0, y = 0):
        for xx in range(x, x + (len(text) * 8)):
            for yy in range(y, y + 8):
                self.display.pixel(xx, yy, 0)
        self.display.text(text, x, y)

    def hex2bits(self, hexstr):
        bitstr = ""
        for pos in range(0, len(hexstr) - 1, 2):
            newhex = hexstr[pos:pos + 2]
            newint = int(newhex, 16)
            newbin = bin(newint)[2:]
            newbits = '0' * (8 - len(newbin)) + newbin
            bitstr += newbits
        return bitstr

    def oled_graphic(self, file, origin_x = 0, origin_y = 0):
        pic = [line.rstrip('\r\n') for line in open(file)]
        for y, row in enumerate(pic):
            line = self.hex2bits(row)
            for x, col in enumerate(line):            
                if col == "1":
                    self.display.pixel(origin_x + x, origin_y + y, 1)
                else:
                    self.display.pixel(origin_x + x, origin_y + y, 0)


    def oled_line(self, x1, y1, x2, y2, col=1):
        dx = x2 - x1
        dy = y2 - y1
     
        is_steep = abs(dy) > abs(dx)
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
     
        swapped = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            swapped = True
     
        dx = x2 - x1
        dy = y2 - y1
     
        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1
     
        y = y1
        points = []
        for x in range(x1, x2 + 1):
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx
     
        if swapped:
            points.reverse()

        for point in points:
            self.display.pixel(point[0], point[1], col)

    def oled_circle(self, x0, y0, radius, col=1):
        x = radius
        y = 0
        err = 0

        while x >= y:
            self.display.pixel(x0 + x, y0 + y, col)
            self.display.pixel(x0 + y, y0 + x, col)
            self.display.pixel(x0 - y, y0 + x, col)
            self.display.pixel(x0 - x, y0 + y, col)
            self.display.pixel(x0 - x, y0 - y, col)
            self.display.pixel(x0 - y, y0 - x, col)
            self.display.pixel(x0 + y, y0 - x, col)
            self.display.pixel(x0 + x, y0 - y, col)

            y += 1
            err += 1 + 2*y
            if 2*(err-x) + 1 > 0:
                x -= 1
                err += 1 - 2*x    

    def oled_box(self, x1, y1, x2, y2, col=1):
        for x in range(x1, x2):
            self.display.pixel(x, y1, col)
            self.display.pixel(x, y2, col)
        for y in range(y1, y2):
            self.display.pixel(x1, y, col)
            self.display.pixel(x2, y, col)
            
    def oled_block(self, x1, y1, x2, y2, col=1):
        for x in range(x1, x2):
            for y in range(y1, y2):
                self.display.pixel(x, y, col)

    # NeoPixel control

    def pixel_color(self, red, green, blue):
        self.np[0] = (red, green, blue)
        self.np.write()
        time.sleep_ms(50)
        self.np[0] = (red, green, blue)
        self.np.write()

    # Input buttons

    def button_pressed(self, pin):
        if pin.value() == 0:
            active = 0
            while pin.value() == 0 and active < 75:
                active += 1
                time.sleep_ms(1)
            if pin.value() == 0 and active >= 75:
                self.buzzer_play(1000, 128, 50)
                return True
            else:
                return False
        else:
            return False
        
    def button1_pressed(self):
        return self.button_pressed(self.button1)

    def button2_pressed(self):
        return self.button_pressed(self.button2)

    def button3_pressed(self):
        return self.button_pressed(self.button3)

    # Piezo speaker

    def buzzer_play(self, freq, duty, duration):
        self.buzzer.freq(freq)
        self.buzzer.duty(duty)
        time.sleep_ms(duration)
        self.buzzer.deinit()



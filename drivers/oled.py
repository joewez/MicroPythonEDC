import machine
import framebuf
from drivers import font454

class OLED:
    _byte = bytearray(1)
    _word = bytearray(2)

    def __init__(self, sdaPin, sclPin, width, height, address=0x3c):
        self._i2c = machine.I2C(sda=machine.Pin(sdaPin), scl=machine.Pin(sclPin))
        self._address = address
        self.width = width
        self.height = height
        pages = height // 8

        self._command = bytearray(b'\x21\x00\x7f\x22\x00\x0f')
        self._command[2] = width - 1
        if width == 64:
            self._command[1] += 32
            self._command[2] += 32
        self._command[5] = pages - 1
        self._i2c.writeto_mem(self._address, 0x00, b'\xae\x20\x00\x40\x00\xa1'
                              b'\xc8\xd3\x00\xd5\x80\xd9\xf1\xdb\x30\x8d\x14'
                              b'\x81\xff\xa4\xa6')
        self._word[0] = 0xa8
        self._word[1] = height - 1
        self._i2c.writeto_mem(self._address, 0x00, self._word)
        self._word[0] = 0xda
        self._word[1] = 0x02 if height == 32 else 0x12
        self._i2c.writeto_mem(self._address, 0x00, self._word)
        self.active(True)

        buffer = bytearray(width * pages)
        self.fb = framebuf.FrameBuffer(buffer, width, height, framebuf.MVLSB)
        self._buffer = buffer

    def active(self, val):
        self._i2c.writeto_mem(self._address, 0x00, b'\xaf' if val else b'\xae')

    def inverse(self, val):
        self._i2c.writeto_mem(self._address, 0x00, b'\xa7' if val else b'\xa6')

    def vscroll(self, dy):
        self._byte[0] = 0x40 | dy & 0x3f
        self._i2c.writeto_mem(self._address, 0x00, self._byte)

    def flip(self, val):
        self._i2c.writeto_mem(self._address, 0x00, b'\xc0' if val else b'\xc8')

    def mirror(self, val):
        self._i2c.writeto_mem(self._address, 0x00, b'\xa0' if val else b'\xa1')

    def contrast(self, val):
        self._word[0] = 0x81
        self._word[1] = val & 0xff
        self._i2c.writeto_mem(self._address, 0x00, self._word)

    def update(self):
        self._i2c.writeto_mem(self._address, 0x00, self._command)
        self._i2c.writeto_mem(self._address, 0x40, self._buffer)

    def clear(self, col=0):
        self.fb.fill(col)

    def show(self):
        self.update()

    def pixel(self, x, y, col):
        self.fb.pixel(x, y, col)

    def text(self, text, x=0, y=0):
        self.fb.fill_rect(x, y, 8 * len(text), 8, 0)
        self.fb.text(text, x, y)

    def smalltext(self, text, x=0, y=0):
        self.fb.fill_rect(x, y, 4 * len(text), 6, 0)
        font454.text(self.fb, text, x, y)

    def line(self, x1, y1, x2, y2, col=1):
        self.fb.line(x1, y1, x2, y2, col)

    def circle(self, x0, y0, radius, col=1):
        x = radius
        y = 0
        err = 0

        while x >= y:
            self.fb.pixel(x0 + x, y0 + y, col)
            self.fb.pixel(x0 + y, y0 + x, col)
            self.fb.pixel(x0 - y, y0 + x, col)
            self.fb.pixel(x0 - x, y0 + y, col)
            self.fb.pixel(x0 - x, y0 - y, col)
            self.fb.pixel(x0 - y, y0 - x, col)
            self.fb.pixel(x0 + y, y0 - x, col)
            self.fb.pixel(x0 + x, y0 - y, col)

            y += 1
            err += 1 + 2*y
            if 2*(err-x) + 1 > 0:
                x -= 1
                err += 1 - 2*x    
    
    def box(self, x, y, width, height, col=1):
        self.fb.rect(x, y, width, height, col)

    def hex2bits(self, hexstr):
        bitstr = ""
        for pos in range(0, len(hexstr) - 1, 2):
            newhex = hexstr[pos] + hexstr[pos + 1]
            newint = int(newhex, 16)
            newbin = bin(newint)[2:]
            newbits = '0' * (8 - len(newbin)) + newbin
            bitstr += newbits
        return bitstr

    def graphic(self, file, origin_x = 0, origin_y = 0, erase = False):
        pic = [line.rstrip('\r\n') for line in open(file)]
        for y, row in enumerate(pic):
            line = self.hex2bits(row)
            for x, col in enumerate(line):
                if erase:
                    self.fb.pixel(origin_x + x, origin_y + y, 0)
                else:
                    self.fb.pixel(origin_x + x, origin_y + y, int(col))

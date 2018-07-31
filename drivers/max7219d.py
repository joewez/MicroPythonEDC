from machine import Pin

class Max7219D:
    
    NO_DECODE = 0x00    # no decode mode value for the decode register
    CODEB = 0xFF        # code B mode value for the decode register
    
    OFF = 0x00            # display off value for the shutdown register
    ON = 0x01            # display on value for the shutdown register
    
    NOTEST = 0x00        # normal operation value for the test register
    DOTEST = 0x01        # test mode value for the test register
    
    # Address of the MAX7219 d-registers
    register = {
        # Digit value registers.
        # In NO_DECODE mode, the format is: dp a b c d e f g
        #     aa
        #   f    b
        #   f    b
        #     gg
        #   e    c
        #   e    c
        #     dd   dp
        #
        # In CODEB mode, the following is displayed according to the value of the register:
        # 0x00 : 0
        # 0x01 : 1
        # 0x02 : 2
        # 0x03 : 3
        # 0x04 : 4
        # 0x05 : 5
        # 0x06 : 6
        # 0x07 : 7
        # 0x08 : 8
        # 0x09 : 9
        # 0x0A : -
        # 0x0B : E
        # 0x0C : H
        # 0x0D : L
        # 0x0E : P
        # 0x0F : <blank>
        'digit'     : (0x08, 0x07, 0x06, 0x05, 0x04, 0x03, 0x02, 0x01),
        # Decode register. Its value sets the decode mode (NO_DECODE or CODEB)
        'decode'    : 0x09,
        # Intensity register. Set the duty cycle from 1/32 for 0x00 to 31/32 for 0x0F
        'intensity' : 0x0A,
        # Scan limit register. Display digit 0 only for 0x00, digits 0 to 7 for 0x07
        'scanlimit' : 0x0B,
        # Shutdown register. Sets the MAX7219 display on (ON) or off (OFF)
        'shutdown'  : 0x0C,
        # Test register. Puts the MAX7219 in test mode (DOTEST) or in normal operation (NOTEST)
        'test'      : 0x0F
    }
    
    def __init__(self, spi, cs):
        self.spi = spi
        self.cs = cs
        self.cs.init(Pin.OUT)
        self.buffer = bytearray(2)
    
    def deinit(self):
        self.spi.deinit()
        self.cs.init(Pin.IN)
    
    def send(self, register, data):
        self.buffer[0] = register
        self.buffer[1] = data
        self.spi.write(self.buffer)
        self.cs.on()
        self.cs.off()
    
    def digit(self, number, value):
        self.send(Max7219D.register['digit'][number], value)
    
    def decode(self, code):
        self.send(Max7219D.register['decode'], code)
    
    def intensity(self, percent):
        self.send(Max7219D.register['intensity'], int((percent * 15)/100))
    
    def scan(self, dig_num):
        self.send(Max7219D.register['scanlimit'], dig_num - 1)
    
    def switch(self, mode):
        self.send(Max7219D.register['shutdown'], mode)
    
    def test(self, test):
        self.send(Max7219D.register['test'], test)

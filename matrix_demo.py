import urandom
from shields import matrixled_shield

def demo():
    matrix = matrixled_shield.MatrixLED_Shield()
    while True:
        effect = urandom.getrandbits(3)
        if effect == 0:
            FillAndEmpty(matrix)
        elif effect == 1:
            Raindrop(matrix)
        elif effect == 2:
            Blackdrop(matrix)
        elif effect == 3:
            Tunnel(matrix)            
        elif effect == 4:
            AntiTunnel(matrix)            
        elif effect == 5:
            Checkerboard(matrix)
        elif effect == 6:
            PartialFill(matrix)
        else:
            Blink(matrix)

def Fill(matrix):
    matrix.clear()
    for x in range(0, 8):
        for y in range(0, 8):
            matrix.pixel(x, y, 1)
    matrix.show()

def Unfill(matrix):
    matrix.clear()
    matrix.show()

def FillAndEmpty(matrix):
    matrix.clear()
    for x in range(0, 8):
        for y in range(0, 8):
            matrix.pixel(x, y, 1)
            matrix.show()
    for x in range(0, 8):
        for y in range(0, 8):
            matrix.pixel(x, y, 0)
            matrix.show()

def Raindrop(matrix):
    matrix.clear()
    count = urandom.getrandbits(6)
    for i in range(0, count):
        x = urandom.getrandbits(3)
        y = urandom.getrandbits(3)
        matrix.pixel(x, y, 1)
        matrix.show()

def Blackdrop(matrix):
    Fill(matrix)
    count = urandom.getrandbits(6)
    for i in range(0, count):
        x = urandom.getrandbits(3)
        y = urandom.getrandbits(3)
        matrix.pixel(x, y, 0)
        matrix.show()

def Blink(matrix):
    times = urandom.getrandbits(2)
    for i in range(times):
        Fill(matrix)
        Unfill(matrix)

def Tunnel(matrix):
    times = urandom.getrandbits(2)
    for j in range(times):
        matrix.clear()
        for k in range(3):
            low = k
            high = 7 - k
            for y in range(low, high + 1):
                matrix.pixel(low, y)
            for x in range(low, high + 1):
                matrix.pixel(x, high)
            for y in range(high + 1, low, -1):
                matrix.pixel(high, y)
            for x in range(high + 1, low, -1):
                matrix.pixel(x, low)
            matrix.show()

def AntiTunnel(matrix):
    times = urandom.getrandbits(2)
    for j in range(times):
        Fill(matrix)
        for k in range(3):
            low = k
            high = 7 - k
            for y in range(low, high + 1):
                matrix.pixel(low, y, 0)
            for x in range(low, high + 1):
                matrix.pixel(x, high, 0)
            for y in range(high + 1, low, -1):
                matrix.pixel(high, y, 0)
            for x in range(high + 1, low, -1):
                matrix.pixel(x, low, 0)
            matrix.show()

def Checkerboard(matrix):
    for z in range(3):
        matrix.clear()
        for x in range(0, 8):
            for y in range(0, 8):
                matrix.pixel(x, y, (x + y) % 2)
            matrix.show()
        for x in range(0, 8):
            for y in range(0, 8):
                if (x + y) % 2 == 0:
                    matrix.pixel(x, y, 1)
                else:
                    matrix.pixel(x, y, 0)
            matrix.show()

def PartialFill(matrix):
    matrix.clear()
    for x in range(0, 8):
        top = urandom.getrandbits(3)
        for y in range(0, top):
            matrix.pixel(x, y, 1)
            matrix.show()


demo()
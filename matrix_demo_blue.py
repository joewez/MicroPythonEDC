import urandom
from shields import ht16k33_shield
import time

delay = 40

def demo():
    matrix = ht16k33_shield.HT16K33_Shield()
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
    matrix.fill(0)
    for x in range(0, 8):
        for y in range(0, 8):
            matrix.pixel(x, y, 1)
            matrix.show()
            time.sleep_ms(delay)


def Unfill(matrix):
    matrix.fill(1)
    for x in range(0, 8):
        for y in range(0, 8):
            matrix.pixel(x, y, 0)
            matrix.show()
            time.sleep_ms(delay)

def FillAndEmpty(matrix):
    matrix.clear()
    for x in range(0, 8):
        for y in range(0, 8):
            matrix.pixel(x, y, 1)
            matrix.show()
            time.sleep_ms(delay)
    for x in range(0, 8):
        for y in range(0, 8):
            matrix.pixel(x, y, 0)
            matrix.show()
            time.sleep_ms(delay)

def Raindrop(matrix):
    matrix.fill(0)
    count = urandom.getrandbits(6)
    for i in range(0, count):
        x = urandom.getrandbits(3)
        y = urandom.getrandbits(3)
        matrix.pixel(x, y, 1)
        matrix.show()
        time.sleep_ms(delay)

def Blackdrop(matrix):
    matrix.fill(1)
    count = urandom.getrandbits(6)
    for i in range(0, count):
        x = urandom.getrandbits(3)
        y = urandom.getrandbits(3)
        matrix.pixel(x, y, 0)
        matrix.show()
        time.sleep_ms(delay)

def Blink(matrix):
    times = urandom.getrandbits(2)
    for i in range(times):
        Fill(matrix)
        Unfill(matrix)

def Tunnel(matrix):
    times = urandom.getrandbits(2)
    for j in range(times):
        matrix.fill(0)
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
            time.sleep_ms(delay)

def AntiTunnel(matrix):
    times = urandom.getrandbits(2)
    for j in range(times):
        matrix.fill(1)
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
            time.sleep_ms(delay)

def Checkerboard(matrix):
    for z in range(3):
        matrix.fill(0)
        for x in range(0, 8):
            for y in range(0, 8):
                matrix.pixel(x, y, (x + y) % 2)
            matrix.show()
            time.sleep_ms(delay)
        for x in range(0, 8):
            for y in range(0, 8):
                if (x + y) % 2 == 0:
                    matrix.pixel(x, y, 1)
                else:
                    matrix.pixel(x, y, 0)
            matrix.show()
            time.sleep_ms(delay)

def PartialFill(matrix):
    matrix.fill(0)
    for x in range(0, 8):
        top = urandom.getrandbits(3)
        for y in range(0, top):
            matrix.pixel(x, y, 1)
            matrix.show()
            time.sleep_ms(delay)

demo()
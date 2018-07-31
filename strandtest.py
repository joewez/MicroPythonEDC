import machine
import neopixel
import time
import urandom

pixel_pin = 4
pixel_count = 14

pin = machine.Pin(pixel_pin, machine.Pin.OUT)
np = neopixel.NeoPixel(pin, pixel_count)

def colorWipe(color, wait):
    for n in range(pixel_count):
        np[n] = color
        np.write()
        time.sleep_ms(wait)

def randomXmasColor():
    emphasis = urandom.getrandbits(2)
    if emphasis == 0:
        red = urandom.getrandbits(8)
        green = urandom.getrandbits(4)
        blue = urandom.getrandbits(4)
    elif emphasis == 1:
        red = urandom.getrandbits(4)
        green = urandom.getrandbits(8)
        blue = urandom.getrandbits(4)
    elif emphasis == 2:
        red = urandom.getrandbits(4)
        green = urandom.getrandbits(4)
        blue = urandom.getrandbits(8)
    else:
        red = urandom.getrandbits(4)
        green = urandom.getrandbits(4)
        blue = urandom.getrandbits(4)
    return (red, green, blue)

def randomWipe(wait):
    for n in range(pixel_count):
        np[n] = randomXmasColor()
        np.write()
        time.sleep_ms(wait)

def theaterChase(color, wait):
    for j in range(10):
        for q in range(3):
            for i in range(0, pixel_count, 3):
                np[i + q] = color
            np.write()
            time.sleep_ms(wait)
            for i in range(0, pixel_count, 3):
                np[i + q] = (0, 0, 0)
            np.write()

def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

def rainbow(wait):
    for j in range(256):
        for i in range(pixel_count):
            np[i] = wheel((i + j) & 255)
        np.write()
        time.sleep_ms(wait)

def rainbowCycle(wait):
    for j in range(256*5):
        for i in range(pixel_count):
            np[i] = wheel((int(i * 256 / pixel_count) + j) & 255)
        np.write()
        time.sleep_ms(wait)

def theaterChaseRainbow(wait):
    for j in range(256):
        for q in range(3):
            for i in range(0, pixel_count, 3):
                np[i + q] = wheel((i + j) % 255)
            np.write()
            time.sleep_ms(wait)
            for i in range(0, pixel_count, 3):
                np[i + q] = (0, 0, 0)
            np.write()

def throb(color, wait):
    newcolor = color
    for i in range(60):
        offset = 3
        red = newcolor[0] - offset 
        green = newcolor[1] - offset
        blue = newcolor[2] - offset
        newcolor = (max(red, 0), max(green, 0), max(blue, 0))
        print("down-{}".format(newcolor))
        for n in range(pixel_count):
            np[n] = newcolor
        np.write()
        time.sleep_ms(wait)
    for i in range(60):
        offset = 3
        red = newcolor[0] + offset
        green = newcolor[1] + offset
        blue = newcolor[2] + offset
        newcolor = (min(red, 255), min(green, 255), min(blue, 255))
        print("up-{}".format(newcolor))
        for n in range(pixel_count):
            np[n] = newcolor
        np.write()
        time.sleep_ms(wait)
    for i in range(60):
        offset = 3
        red = newcolor[0] - offset 
        green = newcolor[1] - offset
        blue = newcolor[2] - offset
        newcolor = (max(red, 0), max(green, 0), max(blue, 0))
        print("down-{}".format(newcolor))
        for n in range(pixel_count):
            np[n] = newcolor
        np.write()
        time.sleep_ms(wait)

while True:
    throb((0, 255, 0) , 10)
    throb((127, 127, 0), 10)
    throb((0, 0, 255), 10)

    colorWipe((255, 0, 0), 100)
    colorWipe((0, 255, 0), 100)
    colorWipe((0, 0, 255), 100)
    colorWipe((0, 128, 255), 100)

    randomWipe(100)
    randomWipe(100)
    randomWipe(100)
    time.sleep(10)

    if pixel_count >= 12:
        theaterChase((127, 127, 127), 100)
        theaterChase((127, 0, 0), 100)
        theaterChase((0, 0, 127), 100)

    rainbow(50)
    rainbowCycle(50)

    if pixel_count >= 12:
        theaterChaseRainbow(100)



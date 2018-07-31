from drivers import neopixelstrip
import time

nps = neopixelstrip.NeoPixelStrip(4, 7)
nps.off()
nps.mix()

colors = ((128,0,0), (0, 128, 0), (0, 0, 128), (0, 128, 128), (128, 128, 0), (128, 0, 128))

def run():
    while True:
        nps.mix()
        time.sleep(1)

def fade():
    direction = -8
    offset = 0
    while True:
        if offset <= -128:
            direction = 8
        if offset >= 0:
            direction = -8
        offset += direction
        print(offset)
        for c in colors:
            for i in range(7):
                r = c[0] + offset if c[0] > 0 else 0
                g = c[1] + offset if c[1] > 0 else 0
                b = c[2] + offset if c[2] > 0 else 0
                nps.set_pixel(i, r, g, b)
                time.sleep_ms(50)

def beat(delay):
    while True:
        nps.set_pixel(0, 0, 0, 128)
        time.sleep_ms(delay)
        nps.pixel_off(0)
        time.sleep_ms(delay)


def gradient(start, end):
    dr = start[0] - end[0];
    dg = start[1] - end[1];
    db = start[2] - end[2];

    for i in range(7):
        part = i / 8
        gr = start[0] - (dr * part)
        gg = start[1] - (dg * part)
        gb = start[2] - (db * part)
        nps.set_pixel(0, int(gr), int(gg), int(gb))

run()
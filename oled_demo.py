import urandom
from drivers import oled

display = oled.OLED(4, 5, 64, 48)

while True:

    display.clear()
    for i in range(0, 20):
        x = urandom.getrandbits(6)
        y = urandom.getrandbits(5) + urandom.getrandbits(4)
        display.smalltext('Hello', x, y)
        display.show()

    display.clear()
    for i in range(0, 30):
        x1 = urandom.getrandbits(6)
        y1 = urandom.getrandbits(5) + urandom.getrandbits(4)
        x2 = urandom.getrandbits(6)
        y2 = urandom.getrandbits(5) + urandom.getrandbits(4)
        display.line(x1, y1, x2, y2)
        display.show()

    display.clear()
    for i in range(0, 30):
        x = urandom.getrandbits(6)
        y = urandom.getrandbits(5) + urandom.getrandbits(4)
        display.graphic('/graphics/heartbeat.txt', x, y)
        display.show()

    display.clear()
    for i in range(0, 30):
        x1 = urandom.getrandbits(6)
        y1 = urandom.getrandbits(5) + urandom.getrandbits(4)
        x2 = urandom.getrandbits(6)
        y2 = urandom.getrandbits(5) + urandom.getrandbits(4)
        display.box(x1, y1, x2, y2)
        display.show()

    display.clear()
    for i in range(0, 30):
        x = urandom.getrandbits(6)
        y = urandom.getrandbits(5) + urandom.getrandbits(4)
        display.graphic('/graphics/degree.txt', x, y)
        display.show()

    display.clear()
    for i in range(0, 30):
        x1 = urandom.getrandbits(6)
        y1 = urandom.getrandbits(5) + urandom.getrandbits(4)
        r = urandom.getrandbits(6)
        display.circle(x1, y1, r)
        display.show()

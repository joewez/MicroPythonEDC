import urandom
from drivers import oled
from drivers import wemos

display = oled.OLED(wemos.D3, wemos.D4, 128, 64)

while True:

    display.clear()
    for i in range(0, 20):
        x = urandom.getrandbits(7)
        y = urandom.getrandbits(6)
        display.text('Hello', x, y)
        display.show()

    display.clear()
    for i in range(0, 30):
        x1 = urandom.getrandbits(7)
        y1 = urandom.getrandbits(6)
        x2 = urandom.getrandbits(7)
        y2 = urandom.getrandbits(6)
        display.line(x1, y1, x2, y2)
        display.show()

    display.clear()
    for i in range(0, 30):
        x = urandom.getrandbits(7)
        y = urandom.getrandbits(6)
        display.graphic('/graphics/heartbeat.txt', x, y)
        display.show()

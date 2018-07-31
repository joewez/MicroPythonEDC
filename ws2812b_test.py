import time
from shields import ws2812b_shield

pixel = ws2812b_shield.WS2812B_Shield()

while True:
    pixel.red()
    time.sleep(1)
    pixel.white()
    time.sleep(1)
    pixel.blue()
    time.sleep(1)
    pixel.green()
    time.sleep(1)
    pixel.off()
    time.sleep(1)

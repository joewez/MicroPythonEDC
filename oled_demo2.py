from drivers import oled
import os
import time

display = oled.OLED(4, 5, 64, 48)

files = os.listdir('/graphics')

for i in range(len(files)):
    display.clear()
    display.graphic('/graphics/{}'.format(files[i]))
    display.show()
    time.sleep(5)

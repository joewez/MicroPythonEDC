import time
from drivers import oled
from shields import bmp180_shield

# create object to retrieve the temp
bmp = bmp180_shield.BMP180_Shield()

# create object to work with display
oled_shield = oled.OLED(0, 2, 128, 64)

# flag to toggle heartbeat
beat = True

#root path for graphic files
graphics_root = '/graphics'

def numfile(num):
    return graphics_root + '/n' + str(num) + '.txt'

def gfxfile(name):
    return graphics_root + '/' + name + '.txt'

#pre-compute some non-changing strings
degree_gfx_file = gfxfile('degree')
heartbeat_gfx_file = gfxfile('heartbeat')

# wait for the first check
time.sleep_ms(750)

# infinite loop
while True:

    temp = bmp.farenheit()
    print(temp)

    #offset
    temp -= 10.0

    # we can only display up to 99
    temp = min(temp, 99.00)

    oled_shield.clear()
    
    # draw the temperature display
    itemp = int(temp)
    oled_shield.graphic(numfile(itemp // 10), 4, 8)
    oled_shield.graphic(numfile(itemp % 10), 28, 8)
    oled_shield.graphic(degree_gfx_file, 53, 4)
    oled_shield.box(0, 0, 63, 47)
    
    # toggle the heartbeat graphic
    if beat:
        oled_shield.graphic(heartbeat_gfx_file, 53, 38)
        beat = False
    else:
        oled_shield.graphic(heartbeat_gfx_file, 53, 38, erase=True)
        beat = True

    oled_shield.show()

    # wait for the next check
    time.sleep_ms(1000)
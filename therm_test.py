import time
from drivers import oled
from shields import ds18b20_shield

# create object to work with display
oled_shield = oled.OLED(0, 2, 128, 64)

# create object to retrieve the temp
ds_shield = ds18b20_shield.DS18B20_Shield()

# infinite loop
while True:

    temp = ds_shield.farenheit()
    print(temp)

    #offset
    temp -= 10.0

    oled_shield.clear()
    oled_shield.text(str(temp))
    oled_shield.show()

    # wait for the next check
    time.sleep_ms(2000)
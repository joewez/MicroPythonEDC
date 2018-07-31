import time
from shields import ds18b20_shield

# create object to retrieve the temp
ds_shield = ds18b20_shield.DS18B20_Shield()

# infinite loop
while True:

    temp = ds_shield.farenheit()

    #offset
    temp -= 10.0

    print(temp)

    # wait for the next check
    time.sleep_ms(2000)
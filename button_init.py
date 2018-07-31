# system startup modes
# routines to control operation based on button pressed on boot
# Author: JGWezensky

# shutdown the Wifi on the chip
import wifi
wifi.none()

import time
time.sleep(5)

# check the status of the buttons
import machine
left = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
right = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)

leftval = not left.value()
rightval = not right.value()

if leftval:
    print('left')
    from connect import home
    time.sleep(10)
    import uftpd
elif rightval:
    print('right')
    wifi.access_point('pocketcloud')
    time.sleep(10)
    import uhttp
    uhttp.start()
    wifi.none()

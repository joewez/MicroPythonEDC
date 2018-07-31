# simple scan of available WiFi access points
# just import to run

import network
import time
import esp

def scan():
    esp.osdebug(None)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    time.sleep(2)
    print('Scanning...')
    nets = wlan.scan()
    for net in nets:
        print(' ' + str(net[0], "utf-8"))
    wlan.active(False)
    esp.osdebug(0)

scan()
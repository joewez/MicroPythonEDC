# initialize a wiFi connection among multiple ssids
#

from aps_trusted import APS
from network import WLAN, STA_IF
from esp import osdebug
from time import sleep_ms

def try_connection():
    t = 12
    while not wlan.isconnected() and t > 0:
        print('.', end='')
        sleep_ms(500)
        t = t - 1
    return wlan.isconnected()

# make the output clean for now
osdebug(None)

# activate the station connect
wlan = WLAN(STA_IF)
wlan.active(True)

# see if we can get a connection with the current settings
print('Connecting to last AP ', end='')
print(try_connection())
if not wlan.isconnected():
    ## find all APs
    ap_list = wlan.scan()
    ## sort APs by signal strength
    ap_list.sort(key=lambda ap: ap[3], reverse=True)
    ## filter only trusted APs
    ap_list = list(filter(lambda ap: ap[0].decode('UTF-8') in 
              APS.keys(), ap_list))
    for ap in ap_list:
        essid = ap[0].decode('UTF-8')
        if not wlan.isconnected():
            print('connecting to new AP', essid, end='')
            wlan.connect(essid, APS[essid])
            print(try_connection())

import gc
gc.collect()
osdebug(0)

import network

def connect(ssid, password=""):
    ap = network.WLAN(network.AP_IF)    
    ap.active(False)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass

    print('network config:', wlan.ifconfig())

def disconnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    while wlan.isconnected():
        pass

    print('disconnected.')

def access_point(ssid, passphrase=""):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    while wlan.isconnected():
        pass

    ap = network.WLAN(network.AP_IF)    
    ap.active(True)
    if (passphrase == ''):
        ap.config(essid=ssid, password="", authmode=1)
    else:
        ap.config(essid=ssid, password=passphrase, authmode=4)

    print('network config:', ap.ifconfig())

def none():
    ap = network.WLAN(network.AP_IF)    
    ap.active(False)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    while wlan.isconnected():
        pass

    print('wifi off')

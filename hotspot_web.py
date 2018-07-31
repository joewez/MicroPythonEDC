# hotspot_web.py
# Script to start a standalone web server

import wifi
import time

print('Starting AP...')
wifi.none()
wifi.access_point('pocketcloud')
time.sleep(5)

print('Starting web server...')
import captive_server

print('Shutting down WiFi.')
wifi.none()
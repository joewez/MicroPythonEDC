# hotspot_ftp.py
# Script to start a standalone ftp server

import wifi
import time

print('Starting AP...')
wifi.none()
wifi.access_point('pocketcloud')
time.sleep(5)

print('Starting ftp server...')
import uftpd
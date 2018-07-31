# Utilities for working with the network
# Author: Joseph G. Wezensky
# License: MIT License (https://opensource.org/licenses/MIT)

def wget(url, filespec):
    import socket
    f = open(filespec, 'w')
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            f.write(data)
        else:
            break
    s.close()
    f.close()

def status():
    import network
    ap = network.WLAN(network.AP_IF)
    print('AP :{0}'.format(ap.active()))

    sta = network.WLAN(network.STA_IF)
    print('STA:{0}'.format(sta.active()))
    if (sta.active()):
        (address, mask, gateway, dns) = sta.ifconfig()
        print('IP :{0}'.format(address))
        print('GW :{0}'.format(gateway))
        print('DNS:{0}'.format(dns))
    ma = ":".join(map(lambda x: "%02x" % x, sta.config('mac')))
    print('MAC:{0}'.format(ma))

def sync_rtc():
    from ntptime import settime
    settime()

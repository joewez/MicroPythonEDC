# Captive portal for serving a web site
# Author: Joseph G. Wezensky
# License: MIT License (https://opensource.org/licenses/MIT)

# Note:
# This script assumes that the ESP is already configured as an AP

import uasyncio as asyncio
import uos
import socket
import network
import dnsquery

webroot = 'wwwroot'
default = 'index.html'
redirect_file = '/misc/portal.html'

@asyncio.coroutine
def capture_dns(udps, ip):
    while True:
        try:
            data, addr = udps.recvfrom(1024)
            p=dnsquery.DNSQuery(data)
            udps.sendto(p.respuesta(ip), addr)
        except:
            pass
            #print('no dns')
        await asyncio.sleep_ms(300)

# Breaks an HTTP request into its parts and boils it down to a physical file (if possible)
def decode_path(req):
    cmd, headers = req.decode("utf-8").split('\r\n', 1)
    parts = cmd.split(' ')
    method, path = parts[0], parts[1]
    # remove any query string
    query = ''
    r = path.find('?')
    if r > 0:
        query = path[r:]
        path = path[:r]
    # check for use of default document
    if path == '/':
        path = default
    else:
        path = path[1:]
    # return the physical path of the response file
    return webroot + '/' + path

# Looks up the content-type based on the file extension
def get_mime_type(file):
    if file.endswith(".html"):
        return "text/html", False
    if file.endswith(".css"):
        return "text/css", True
    if file.endswith(".js"):
        return "text/javascript", True
    if file.endswith(".png"):
        return "image/png", True
    if file.endswith(".gif"):
        return "image/gif", True
    if file.endswith(".jpeg") or file.endswith(".jpg"):
        return "image/jpeg", True
    return "text/plain", False

# Quick check if a file exists
def exists(file):
    try:
        s = uos.stat(file)
        return True
    except:
        return False    

@asyncio.coroutine
def serve_http(reader, writer):
    try:
        file = decode_path((yield from reader.read()))

        if exists(file):
            mime_type, cacheable = get_mime_type(file)
            yield from writer.awrite("HTTP/1.0 200 OK\r\n")
            yield from writer.awrite("Content-Type: {}\r\n".format(mime_type))
            if cacheable:
                yield from writer.awrite("Cache-Control: max-age=86400\r\n")
            yield from writer.awrite("\r\n")
        else:
            yield from writer.awrite("HTTP/1.0 200 OK\r\n")
            yield from writer.awrite("Content-Type: text/html\r\n")
            yield from writer.awrite("\r\n")
            file = redirect_file

        print(file)

        buf = bytearray(512)
        f = open(file, "rb")
        size = f.readinto(buf)
        while size > 0:
            yield from writer.awrite(buf, sz=size)
            size = f.readinto(buf)
        f.close()

    except:
        raise
    finally:
        yield from writer.aclose()

def run():
    import logging
    logging.basicConfig(level=logging.ERROR)

    # get the configuration of the ESP8266 as an AP
    ap = network.WLAN(network.AP_IF)
    ip = ap.ifconfig()[0]

    # prepare to capture DNS requests
    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udps.setblocking(False)
    udps.bind(('',53))

    # load up the coros and run
    loop = asyncio.get_event_loop()
    loop.create_task(capture_dns(udps, ip))
    loop.create_task(asyncio.start_server(serve_http, "0.0.0.0", 80, 20))
    loop.run_forever()
    loop.close()

    udps.close()

run()
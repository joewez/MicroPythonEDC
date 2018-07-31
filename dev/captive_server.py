# Captive portal for serving webpages
# Joseph G. Wezensky
#

import uasyncio as asyncio
import uos
import socket
import network
import dnsquery
import gc

webroot = 'wwwroot'
default = 'index.html'

@asyncio.coroutine
def capture_dns():

    ap = network.WLAN(network.AP_IF)
    ip = ap.ifconfig()[0]

    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udps.setblocking(False)
    udps.bind(('',53))

    try:
        while True:
            try:
                data, addr = udps.recvfrom(1024)
                p=dnsquery.DNSQuery(data)
                udps.sendto(p.respuesta(ip), addr)
            except:
                pass
            await asyncio.sleep_ms(300)
    except KeyboardInterrupt:
        print('Closing')
    except:
        print('Exception')

    udps.close()

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
        return "text/html", False, False
    if file.endswith(".css"):
        return "text/css", True, False
    if file.endswith(".js"):
        return "text/javascript", True, False
    if file.endswith(".png"):
        return "image/png", True, True
    if file.endswith(".gif"):
        return "image/gif", True, True
    if file.endswith(".jpeg") or file.endswith(".jpg"):
        return "image/jpeg", True, True
    return "text/plain", False, False

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
        print(file)

        if exists(file):
            yield from writer.awrite("HTTP/1.0 200 OK\r\n")

            mime_type, cacheable, binary = get_mime_type(file)
            yield from writer.awrite("Content-Type: {}\r\n".format(mime_type))
            if cacheable:
                yield from writer.awrite("Cache-Control: max-age=86400\r\n")
            yield from writer.awrite("\r\n")

            if binary:
                f = open(file, "rb")
                buffer = f.read(128)
                while buffer != b'':
                    yield from writer.awrite(buffer)
                    buffer = f.read(128)
                f.close()
            else:
                f = open(file)
                for line in f:
                    yield from writer.awrite(line)
                f.close()

        else:
            yield from writer.awrite("HTTP/1.0 200 OK\r\n")
            yield from writer.awrite("Content-Type: text/html\r\n")
            yield from writer.awrite("\r\n")

            f = open('/misc/redirect.html')
            for line in f:
                yield from writer.awrite(line)
            f.close()

    except:
        raise
    finally:
        yield from writer.aclose()
        gc.collect()

def run():
    import logging
    logging.basicConfig(level=logging.ERROR)

    loop = asyncio.get_event_loop()
    loop.create_task(capture_dns())
    loop.create_task(asyncio.start_server(serve_http, "0.0.0.0", 80, 20))
    loop.run_forever()
    loop.close()

run()
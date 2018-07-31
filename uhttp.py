#
# Simple HTTP server based on the uasyncio example script
# by J.G. Wezensky (joewez@gmail.com)
#

import uasyncio as asyncio
import uos
import pkg_resources

webroot = 'wwwroot'
default = 'index.html'

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
def serve(reader, writer):
    try:
        file = decode_path((yield from reader.read()))
        if exists(file):
            mime_type, cacheable = get_mime_type(file)
            yield from writer.awrite("HTTP/1.0 200 OK\r\n")
            yield from writer.awrite("Content-Type: {}\r\n".format(mime_type))
            if cacheable:
                yield from writer.awrite("Cache-Control: max-age=86400\r\n")
            yield from writer.awrite("\r\n")

            f = open(file, "rb")
            buffer = f.read(512)
            while buffer != b'':
                yield from writer.awrite(buffer)
                buffer = f.read(512)
            f.close()
        else:
            yield from writer.awrite("HTTP/1.0 404 NA\r\n\r\n")
    except:
        raise
    finally:
        yield from writer.aclose()

def start():
    import logging
    logging.basicConfig(level=logging.ERROR)

    loop = asyncio.get_event_loop()
    loop.call_soon(asyncio.start_server(serve, "0.0.0.0", 80, 20))
    loop.run_forever()
    loop.close()

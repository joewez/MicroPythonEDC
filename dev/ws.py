import usocket as socket
import uselect as select
import uio
import utime
import gc

routes = dict()
request = dict()
conns = dict()
server = socket.socket()
selector = select.poll()

def accept(s):
    sock, addr = s.accept()
    sock.setblocking(False)
    selector.register(sock, select.POLLIN)

def read(s):
    r = s.read()
    if r:
        request[id(s)] = request.get(id(s),b'') + r
        if r[-4:] == b'\r\n\r\n':
            req = request.pop(id(s))
            get = req.split(b' ',2)[1].split(b'?',1)
            path = get[0]
            serve = routes.get(path)
            headers = b"HTTP/1.1 200 OK\r\n"
            if type(serve) is bytes:
                if serve[-3:] == b'.gz':
                    headers += b"Content-Encoding: gzip\r\n"
                body = open(serve,'rb')
            elif callable(serve):
                body = uio.BytesIO(serve(*get[1:]) or b'')
            else:
                headers = b"HTTP/1.1 404 Not Found\r\n"
                body = uio.BytesIO(b"")
            headers += "\r\n"
            buf = bytearray(headers+'\x00'*(536-len(headers)))
            bufmv = memoryview(buf)
            bw = body.readinto(bufmv[len(headers):],536-len(headers))
            c = (body,buf,bufmv,[0,len(headers)+bw])
            conns[id(s)] = c
            selector.modify(s, select.POLLOUT)
    else:
        close(s)

def bufferfile(c,w):
    if w == c[3][1] - c[3][0]:
        c[3][0] = 0
        c[3][1] = c[0].readinto(c[1],536)
    else:
        c[3][0] += w
    
def close(s):
    s.close()
    selector.unregister(s)
    sid = id(s)
    if sid in request:
        del request[id(s)]
    if sid in conns:
        del conns[id(s)]
    gc.collect()

@micropython.native
def work(time_ms):
    start = utime.ticks_ms()
    while utime.ticks_diff(utime.ticks_ms(),start) < time_ms:
        ready = selector.poll(time_ms)
        for i in range(len(ready)):
            if ready[i][0] is server:
                accept(ready[i][0])
            elif ready[i][1] & select.POLLOUT:
                s = ready[i][0]
                c = conns[id(s)]
                if c:
                    w = s.write(c[2][c[3][0]:c[3][1]])
                    if not w or c[3][1] < 536:
                        close(s)
                    else:
                        bufferfile(c,w)
            elif ready[i][1] & select.POLLIN:
                read(ready[i][0])

def routefile(path,file):
    routes[path.encode()] = file.encode()
    
def route(path):
    def r(f):
        routes[path.encode()] = f
        return f
    return r

def serve(time_ms=None):
    if time_ms is None:
        while True:
            work(60000)
    else:
        work(time_ms)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(socket.getaddrinfo("0.0.0.0", 80)[0][-1])
server.listen(5)
server.setblocking(False)
selector.register(server, select.POLLIN)
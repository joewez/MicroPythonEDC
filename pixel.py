import socket
import network
import time
import machine
import neopixel
import gc

# setup wifi access point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="pocketcloud", password="", authmode=1) #authmode=1 == no pass

# from the ws2812b rgb shield
pixel_pin = 4
pixel_count = 7

# web server content 
BEGINNING = b"""\
HTTP/1.0 200 OK

<!doctype html>
<html>
    <head>
        <title>Pocket Cloud</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta charset="utf8">
    </head>
    <body>
        <h1>Change My Color!!!</h1>
"""

FORM = b"""\
<form action="/led">
    <p>You are my #{:d} user!</p>
    <table>
        <tr>
            <td><b>Red:</b></td>
            <td>0</td>
            <td><input type="range" min="0" max="255" step="1" name="r" id="r-value" onchange="setColor()" value="{:d}"></td>
            <td>255</td>
            <td rowspan="3"><canvas id="patch" width="100" height="100" style="border:1px solid #000000;" ></canvas></td>
        </tr>
        <tr>
            <td><b>Green:</b></td>
            <td>0</td>
            <td><input type="range" min="0" max="255" step="1" name="g" id="g-value" onchange="setColor()" value="{:d}"></td>
            <td>255</td>
            <td></td>
        </tr>
        <tr>
            <td><b>Blue:</b></td>
            <td>0</td>
            <td><input type="range" min="0" max="255" step="1" name="b" id="b-value" onchange="setColor()" value="{:d}"></td>
            <td>255</td>
            <td></td>
        </tr>
        <tr>
            <td colspan="5" style="text-align: center;" ><input type="submit" value="Change"></td>
        </tr>
    </table>
</form>
"""

ENDING = b"""\
        <script>
            function rgb(r, g, b){
                return "rgb("+r+","+g+","+b+")";
            }

            function setColor() {
                r = document.getElementById('r-value').value;
                g = document.getElementById('g-value').value;
                b = document.getElementById('b-value').value;
                var c = document.getElementById('patch');
                var ctx = c.getContext("2d");
                ctx.beginPath();
                ctx.rect(10, 10, 80, 80);
                ctx.fillStyle = rgb(r, g, b);
                ctx.fill();
            }

            setColor();
        </script>
    </body>
</html>
"""

class DNSQuery:

  def __init__(self, data):
    self.data=data
    self.dominio=''

    #print("Reading datagram data...")
    m = data[2] # ord(data[2])
    tipo = (m >> 3) & 15   # Opcode bits
    if tipo == 0:                     # Standard query
      ini=12
      lon=data[ini] # ord(data[ini])
      while lon != 0:
        self.dominio+=data[ini+1:ini+lon+1].decode("utf-8") +'.'
        ini+=lon+1
        lon=data[ini] #ord(data[ini])

  def respuesta(self, ip):
    packet=b''
    #print("Resposta {} == {}".format(self.dominio, ip))
    if self.dominio:
      packet+=self.data[:2] + b"\x81\x80"
      packet+=self.data[4:6] + self.data[4:6] + b'\x00\x00\x00\x00'   # Questions and Answers Counts
      packet+=self.data[12:]                                         # Original Domain Name Question
      packet+= b'\xc0\x0c'                                             # Pointer to domain name
      packet+= b'\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'             # Response type, ttl and resource data length -> 4 bytes
      packet+=bytes(map(int,ip.split('.'))) # 4 bytes of IP
    return packet

def run_pocket_pixel():

    time.sleep(7)

    pin = machine.Pin(pixel_pin, machine.Pin.OUT)
    np = neopixel.NeoPixel(pin, pixel_count)
    #for n in range(pixel_count):
    #    np[n] = (0, 0, 0)
    #np.write()

    # DNS Server
    ip=ap.ifconfig()[0]
    print('DNS Server: {:s}'.format(ip))

    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udps.setblocking(False)
    udps.bind(('',53))

    # Web Server
    s = socket.socket()
    ai = socket.getaddrinfo(ip, 80)
    print("Web Server: Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    s.settimeout(2)
    print("Web Server: Listening http://{}:80/".format(ip))

    counter = 0

    try:
        while True:
           
            # DNS Loop
            #print("Before DNS...")
            try:
                data, addr = udps.recvfrom(1024)
                #print("incoming datagram...")
                p=DNSQuery(data)
                udps.sendto(p.respuesta(ip), addr)
                #print('Replying: {:s} -> {:s}'.format(p.dominio, ip))
            except:
                #print("No datagram")
                pass

            # Web loop
            #print("before accept...")
            try:
                res = s.accept()
                client_sock = res[0]
                client_addr = res[1]
                #print("Client address:", client_addr)
                #print("Client socket:", client_sock)

                client_stream = client_sock

                #print("Request:")
                req = client_stream.readline()
                print(req)
                while True:
                    h = client_stream.readline()
                    if h == b"" or h == b"\r\n" or h == None:
                        break
                    #print(h)

                # get the current color values
                red, green, blue = np[0]
                
                # Change LED based on request variables
                request_url = req[4:-11]
                api = request_url[:5]
                if api == b'/led?':
                    params = request_url[5:]
                    try:
                        d = {key: value for (key, value) in [x.split(b'=') for x in params.split(b'&')]}
                    except:
                        d = {}

                    if b'r' in d.keys() and b'g' in d.keys() and b'b' in d.keys():
                        
                        red = int(d[b'r'])
                        green = int(d[b'g'])
                        blue = int(d[b'b'])

                        for n in range(pixel_count):
                            np[n] = (red, green, blue)
                        np.write()
                
                        print("Color set to {}".format(np[0]))

                # Send response content
                client_stream.write(BEGINNING)
                client_stream.write(FORM.format(counter, red, green, blue))
                client_stream.write(ENDING)
                client_stream.close()

                counter += 1

            except:
                print("nothing...")

            time.sleep_ms(300)

            gc.collect()

            #print("loop")

    except KeyboardInterrupt:
        print('Closing')

    except:
        print('Exception')

    udps.close()
    s.close()

run_pocket_pixel()
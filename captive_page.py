import socket
import network
import time
import gc
import dnsquery

# setup wifi access point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="pocketcloud", password="", authmode=1) #authmode=1 == no pass

def serve(html_file):

    time.sleep(7)

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
                p=dnsquery.DNSQuery(data)
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

                time.sleep_ms(50)

                # Send response content
                client_stream.write(b'HTTP/1.0 200 OK\r\n')
                client_stream.write(b'\r\n')
                f = open(html_file)
                for line in f.readlines():
                    client_stream.write(line)
                    #print(line)
                f.close()

                client_stream.close()

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

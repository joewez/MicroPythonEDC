import socket
import network
import time
import gc
import dnsquery

def serve():

    ap = network.WLAN(network.AP_IF)
    ip = ap.ifconfig()[0]
    #print('DNS Server: {:s}'.format(ip))

    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udps.setblocking(False)
    udps.bind(('',53))

    try:
        while True:
           
            try:
                data, addr = udps.recvfrom(1024)
                p=dnsquery.DNSQuery(data)
                udps.sendto(p.respuesta(ip), addr)
                #print("..answered request from {:s}".format(addr))
            except:
                pass

            time.sleep_ms(300)
            gc.collect()

    except KeyboardInterrupt:
        print('Closing')

    except:
        print('Exception')

    udps.close()

serve()
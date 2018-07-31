import network
import socket
import ure
import time
import gc

sta = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)

# ------------------------------------------------------
# helper routines for doConfigWork()
# ------------------------------------------------------

def send_response(client, payload, status_code=200):
    client.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
    client.sendall("Content-Type: text/html\r\n")
    client.sendall("Content-Length: {}\r\n".format(len(payload)))
    client.sendall("\r\n")
    
    if len(payload) > 0:
        client.sendall(payload)

# --------------------------------------------------------

def handle_root(client):
    response_header = """
        <h1>ESPWidget Wi-Fi Setup</h1>
        <form action="configure" method="post">
          <label for="ssid">SSID</label>
          <select name="ssid" id="ssid">
    """
    
    response_variable = ""
    turned_on = False
    if not sta.active():
        sta.active(True)
        turned_on = True
    for ssid, *_ in sta.scan():
        response_variable += '<option value="{0}">{0}</option>'.format(ssid.decode("utf-8"))
    if turned_on:
        sta.active(False)

    response_footer = """
           </select> <br/>
           Password: <input name="password" type="password"></input> <br />
           <input type="submit" value="Submit">
         </form>
    """
    send_response(client, response_header + response_variable + response_footer)

# --------------------------------------------------------

def handle_configure(client, request):
    match = ure.search("ssid=([^&]*)&password=(.*)", request)
    
    if match is None:
        send_response(client, "Parameters not found", status_code=400)
        return
    
    ssid = match.group(1)
    password = match.group(2)
    
    if len(ssid) == 0:
        send_response(client, "SSID must be provided", status_code=400)
        return
    
    sta.active(True)
    sta.connect(ssid, password)
    
    send_response(client, "Wi-Fi configured for SSID {}<br />Your widget should now connect...".format(ssid))
    return

# --------------------------------------------------------

def handle_not_found(client, url):
    send_response(client, "Path not found: {}".format(url), status_code=404)

# ------------------------------------------------------------------
# will run the AP and the web server to get the SSID and password
# ------------------------------------------------------------------

def Work(hw):

    hw.pixel_color(64, 0, 0)

    sta.active(False)
    ap.active(True)
    ap.config(essid="ESPWidget", password="thereisnospoon")

    server_socket = socket.socket()
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(addr)
    server_socket.listen(1)

    hw.oled_clear()
    hw.oled_text("Connect to...", 0, 0)
    hw.oled_text("ESPWidget", 16, 12)
    hw.oled_text("Browse to...", 0, 24)
    hw.oled_text("192.168.4.1", 16, 36)
    hw.oled_show()

    while True:
        client, addr = server_socket.accept()
        client.settimeout(5.0)
        
        request = b""
        try:
            while not "\r\n\r\n" in request:
                request += client.recv(512)
        except OSError:
            pass
        
        if "HTTP" not in request:
            client.close()
            continue
        
        url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).rstrip("/")

        finished = False
        if url == "":
            handle_root(client)
        elif url == "configure":
            handle_configure(client, request)
            finished = True
        else:
            handle_not_found(client, url)
        
        client.close()

        if finished:
            hw.oled_clear()
            hw.oled_text("Connecting...", 0, 0)
            hw.oled_show()
            break

    server_socket.close()

    server_socket = None
    client = None
    addr = None
    request = None
    url = None
    finished = None
    gc.collect()

    import machine
    machine.reset()
    

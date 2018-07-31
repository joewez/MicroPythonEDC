import network
import socket
import time
import gc

sta = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)

machine_id = ""
data_host = ""
data_path = ""
data_addr = ""
last_message = ""
error_count = 0
request_count = 0

# ------------------------------------------------------
# helper routines for doWidgetWork()
# ------------------------------------------------------

def setupStatus(hw):
    hw.oled_clear()
    hw.oled_text("STATUS", 40, 0)
    hw.oled_text("UpTime :", 0, 8)
    hw.oled_text("FreeMem:", 0, 16)
    from ubinascii import hexlify
    hw.oled_text("MAC:", 0, 24)
    hw.oled_text(hexlify(sta.config('mac')), 32, 24)
    hw.oled_text("ID:", 0, 32)
    import machine
    hw.oled_text(hexlify(machine.unique_id()), 24, 32)
    hw.oled_text("IP:", 0, 40)
    hw.oled_text("GW:", 0, 48)
    (address, mask, gateway, dns) = sta.ifconfig()
    hw.oled_text(address, 24, 40)
    hw.oled_text(gateway, 24, 48)
    hw.oled_show()
    address = None
    mask = None
    gateway = None
    dns = None
    gc.collect()

def updateStatus(hw):
    hw.oled_text(str(time.time()), 64, 8)
    hw.oled_text(str(gc.mem_free()), 64, 16)
    hw.oled_show()

def setupWidget(hw):
    global data_host
    global data_addr
    global machine_id
    global data_path

    data_host = "wezensky.no-ip.org"
    try:
        data_addr = socket.getaddrinfo(data_host, 80)[0][-1]
    except:
        hw.oled_clear()
        hw.oled_text("Host Not Found", 8, 24)
        hw.oled_show()

    import machine
    from ubinascii import hexlify
    machine_id = hexlify(machine.unique_id()).decode("utf-8")
    data_path = "widget/" + machine_id + "/data.txt"

# --------------------------------------------------------

def updateWidget(hw):
    
    global data_addr
    global data_host
    global data_path
    global error_count
    global last_message
    global request_count

    request_count += 1

    resp = ""
    try:
        s = socket.socket()
        s.connect(data_addr)
        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (data_path, data_host), 'utf8'))
        while True:
            data = s.recv(100)
            if data:
                resp += str(data, 'utf8')
            else:
                break
        s.close()
    except:
        print("HTTP Get failed.")

    if resp == "":
        print("No content retrieved")        
        error_count += 1
        if (error_count > 5):
            print("Sleeping...")
            time.sleep(120)
            error_count = 0
    else:
        #print(resp)
        error_count = 0
        lines = resp.split("\r\n")
        linecount = len(lines)
        content = ""
        if linecount > 0:
            found = False
            for line in range(linecount):
                if lines[line] == "":
                    found = True
                else:
                    if found:
                        content += lines[line]

        if content != "":
            if last_message == "":
                last_message = content
                new_content = True
            else:
                if content == last_message:            
                    new_content = False
                else:
                    last_message = content
                    new_content = True

            if new_content:
                hw.oled_clear()
                commands = content.split("~")
                for command in commands:
                    if command != "":
                        parts = command.split("/")
                        if len(parts) > 0:
                            if parts[0] == "t":
                                hw.oled_text(parts[1], int(parts[2]), int(parts[3]))
                            elif parts[0] == "i":
                                hw.oled_graphic('/graphics/' + parts[1] + '.txt', int(parts[2]), int(parts[3]))
                            elif parts[0] == "l":
                                hw.oled_line(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]))
                            elif parts[0] == "x":
                                hw.oled_box(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]))
                            elif parts[0] == "c":
                                hw.oled_circle(int(parts[1]), int(parts[2]), int(parts[3]))
                            elif parts[0] == "p":
                                hw.pixel_color(int(parts[1]), int(parts[2]), int(parts[3]))
                            elif parts[0] == "s":
                                hw.buzzer_play(int(parts[1]), int(parts[2]), int(parts[3]))
                hw.oled_show()

    resp = None
    s = None
    data = None
    lines = None
    linecount = None
    content = None
    found = None
    new_content = None
    commands = None
    parts = None
    part = None
    line = None
    gc.collect()
    print(gc.mem_free())
    print(request_count)

# --------------------------------------------------------
# will handle the display and the UI for the main function
#---------------------------------------------------------

def Work(hw):

    global last_message
    
    setupWidget(hw)

    current_screen = 0
    refresh_deadline = 0
    while True:
        if current_screen == 0:
            if time.time() > refresh_deadline:
                updateWidget(hw)
                refresh_deadline = time.time() + 15
        elif current_screen == 1:
            updateStatus(hw)

        if hw.button1_pressed():
            if current_screen == 0:
                current_screen = 1
                setupStatus(hw)
            elif current_screen == 1:
                current_screen = 0
                last_message = ""
                updateWidget(hw)

        if hw.button2_pressed():
            if current_screen == 1:
                hw.pixel_color(64, 0, 0)
                sta.disconnect()
                sta.connect("dummy", "")
                sta.active(False)
                break            

        if hw.button3_pressed():
            hw.pixel_color(0, 0, 0)

        gc.collect()

    current_screen = None
    refresh_deadline = None
    gc.collect()
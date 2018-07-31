import time
import rtc
from shields import matrixled_shield
import os
import ntptime
import wifi
import network
from shields import button_buzzer_shield

b = button_buzzer_shield.Button_Buzzer_Shield()
matrix = matrixled_shield.MatrixLED_Shield()
mark_time_file = '\marktime.txt'

def sync_rtc():
    #if not connected():
        #from connect import home
        #time.sleep(30)
    if connected():
        ntptime.settime()

def connected():
    sta = network.WLAN(network.STA_IF)
    return sta.active()

def exists(file):
    try:
        s = os.stat(file)
        return True
    except:
        return False

def start():
    if exists(mark_time_file):
        os.remove(mark_time_file)
    run()

def reset():
    print('Creating new start file...')
    sync_rtc()
    f = open(mark_time_file, "w")
    StartTime = rtc.LocalTime()
    f.write(StartTime)
    f.close()

def run():

    if not exists(mark_time_file):
        reset()

    print('Opening start file...')
    f = open(mark_time_file, "r")
    StartTime = f.read()
    f.close()

    sync_rtc()

    resync_count = 0

    while True:

        display(StartTime, rtc.LocalTime())

        time.sleep(60)

        if (resync_count > 60):
            sync_rtc()
            resync_count = 0
        else:
            resync_count += 1

def display(StartTime, CurrentTime):
    print('Start Time:{0} Current Time:{1}'.format(StartTime, CurrentTime))

    start_hour = int(StartTime[-5:][0:2])
    start_minute = int(StartTime[-5:][3:5])
    current_hour = int(CurrentTime[-5:][0:2])
    current_minute = int(CurrentTime[-5:][3:5])

    #calculate count of 7.5 minute segments that have passed
    if current_minute >= start_minute:
        minute_count = (current_hour - start_hour) * 60
        minute_count += (current_minute - start_minute)
    else:
        minute_count = (current_hour - start_hour) * 60
        minute_count -= (start_minute - current_minute)
    print('minutes ' + str(minute_count))
    total = minute_count / 7.5
    print('total ' + str(total))
    if total > 64:
        done_display()
    else:
        fill_display(64 - total)

def done_display():
    matrix.clear()
    for i in range(8):
        matrix.pixel(i, i, 1)
        matrix.pixel(i, 7 - i, 1)
        matrix.show()

def fill_display(Count):
    matrix.clear()
    for i in range(Count):
        dm = divmod(i, 8)
        matrix.pixel(dm[1], dm[0], 1)
    matrix.show()

#This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
#import webrepl
#webrepl.start()
#import uftpd
#from library import HourlySleeper
#hourly_sleeper = HourlySleeper(1)
gc.collect()
from machine import Timer
import time

counter = 0

def once(self):
    print("once")
    #self.deinit()

def many(self):
    global counter
    counter += 1
    print(counter)

t = Timer(-1)
#t.init(period=10000, mode=Timer.ONE_SHOT, callback=once)
t.init(period=5000, mode=Timer.PERIODIC, callback=many)

while True:
    print("Hello")
    time.sleep(1)

t.deinit()
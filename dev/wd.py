import machine

# Simple WD - Global Variable
wd_feeder = 0 
wd_buffer = 0
wd_counter = 0
wd_threshold = 4

def wd_checker(calledvalue):
    print('watchdog is checking... feeder= {} buffer= {}'.format(wd_feeder, wd_buffer))
    global wd_counter
    global wd_buffer
    global wd_feeder
    if wd_feeder == wd_buffer:
        print('state is suspicious ... counter is {} incrementing the counter'.format(wd_counter))
        wd_counter += 1
    else:
        wd_counter = 0
        wd_feeder = wd_buffer
    if wd_counter == wd_threshold:
        print('Counter is reached its threshold, following function will be called')
        wd_feeder = wd_buffer = wd_counter = 0
        machine.reset()


if __name__ == '__main__':
    scheduler_wd = machine.Timer(-1)
    scheduler_wd.init(period=3000, mode=machine.Timer.PERIODIC, callback=wd_checker)
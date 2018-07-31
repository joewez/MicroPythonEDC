import machine
import time

class Button_Buzzer_Shield():

    def __init__(self):
        self.button1 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
        self.button2 = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
        self.buzzer = machine.PWM(machine.Pin(15))

    def button_pressed(self, pin):
        if pin.value() == 0:
            active = 0
            while pin.value() == 0 and active < 75:
                active += 1
                time.sleep_ms(1)
            if pin.value() == 0 and active >= 75:
                self.buzzer_play(1000, 128, 50)
                return True
            else:
                return False
        else:
            return False

    def button1_state(self):
        return self.button1.value()

    def button1_pressed(self):
        return self.button_pressed(self.button1)

    def button2_pressed(self):
        return self.button_pressed(self.button2)

    def button2_state(self):
        return self.button2.value()

    def buzzer_play(self, freq, duty, duration):
        self.buzzer.freq(freq)
        self.buzzer.duty(duty)
        time.sleep_ms(duration)
        self.buzzer.deinit()


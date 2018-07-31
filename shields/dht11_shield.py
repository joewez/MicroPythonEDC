import machine
import dht

class DHT11_Shield:

    def __init__(self):
        self.pin = machine.Pin(2)
        self.dht = dht.DHT11(self.pin)

    def read_data(self):
        self.dht.measure()
        c = self.dht.temperature()
        f = (c * 1.8) + 32.0
        h = self.dht.humidity()
        return c, f, h

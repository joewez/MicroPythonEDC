import machine
import onewire
import ds18x20

class DS18B20_Shield:

    def __init__(self):
        dat = machine.Pin(4)
        self.ds = ds18x20.DS18X20(onewire.OneWire(dat))
        self.roms = self.ds.scan()

    def celsius(self):
        self.ds.convert_temp()
        return self.ds.read_temp(self.roms[0])

    def farenheit(self):
        return (self.celsius() * 1.8) + 32.0
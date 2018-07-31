class MicroSD_Shield:

    def __init__(self):
        self.mounted = False

    def mount(self):
        if not self.mounted:
            import machine, uos, gc
            from drivers import sdcard
            #print("free={:d}".format(gc.mem_free()))
            gc.collect()
            sd = sdcard.SDCard(machine.SPI(1), machine.Pin(15))
            uos.mount(sd, "/")
            self.mounted = True
            gc.collect()

    def unmount(self):
        if self.mounted:
            import uos, gc
            from flashbdev import bdev
            try:
                gc.collect()
                if bdev:
                    uos.mount(bdev, "/")
                    self.mounted = False
            except OSError:
                import inisetup
                inisetup.setup()
            gc.collect()
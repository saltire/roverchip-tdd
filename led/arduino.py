import time

from serial import Serial


class Arduino:
    def __init__(self, port, baud):
        self.serial = Serial(port, baud, timeout=1)
        time.sleep(2)
        
        
    def write_ints(self, *ints):
        self.serial.write(''.join(chr(i) for i in ints))

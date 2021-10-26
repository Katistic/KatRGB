from enum import Enum
import time
import hid

class Success(Exception):
    pass

class Mode(Enum):
    OFF = 0
    STATIC = 1
    BLINKING = 2
    BREATHING = 3
    COLOUR_CYCLE = 4
    BREATHING_COLOUR_CYCLE = 5

    COLOR_CYCLE = 4
    BREATHING_COLOR_CYCLE = 5

class MP750M:
    def __init__(self):
        self.handle = hid.device()
        self.handle.open(0x2516, 0x0105)

        self.off()

    def off(self):
        self.handle.write([0x0])

    def static(self, red: int, green: int, blue: int):
        self.handle.write([0x0, 0x01, 0x04, red, green, blue])

    def blinking(self, red: int, green: int, blue: int, speed: int):
        self.handle.write([0x0, 0x02, 0x04, red, green, blue, speed])

    def breathing(self, red: int, green: int, blue: int, speed: int):
        self.handle.write([0x0, 0x03, 0x04, red, green, blue, speed])

    def colour_cycle(self, speed: int):
        self.handle.write([0x0, 0x04, 0x01, speed])

    def breathing_colour_cycle(self,):
        self.handle.write([0x0, 0x05])

    def apply(self):
        self.handle.write([0x0, 0x6])

    def read_mode(self) -> Mode:
        self.handle.write([0x0, 0x7])
        return Mode(self.handle.read(3)[2])

    def test(self, data):
        mode = data.pop(0)
        self.handle.write([0x0, mode, len(data)] + data)
        print(data)

    # Alias' -- 
    def color_cycle(self, speed: int):
        self.colour_cycle(speed)

    def breathing_color_cycle(self, speed: int):
        self.breathing_colour_cycle(speed)
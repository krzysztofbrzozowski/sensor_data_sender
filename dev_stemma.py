import time
import board
from adafruit_seesaw.seesaw import Seesaw

i2c_bus = board.I2C()


class STEMMA:
    def __init__(self, addr: int):
        self.sensor = Seesaw(i2c_bus, addr=addr)

    def get_moisture(self):
        return self.sensor.moisture_read()

    def get_temperature(self):
        return self.sensor.get_temp()


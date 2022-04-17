"""
@author:    Krzysztof Brzozowski
@file:      pms_handler
@time:      18/03/2022
@desc:      
"""


import board
from adafruit_seesaw.seesaw import Seesaw


class SensorManager:

    i2c_bus = board.I2C()
    sensor = Seesaw(i2c_bus, addr=addr)

    def __init__(self, addr: int):
        self.sensor = Seesaw(i2c_bus, addr=addr)

    def get_moisture(self):
        return self.sensor.moisture_read()

    def get_temperature(self):
        return self.sensor.get_temp()

    @classmethod
    def get_values(cls):
        """
        Get all values form the sensors (temperature, humidity)
        """
        test_readings = [{'plant': 'a', 'hex_address': 31, 'temperature': 22, 'humidity': 500},
                         {'plant': 'b', 'hex_address': 32, 'temperature': 23, 'humidity': 501},
                         {'plant': 'c', 'hex_address': 33, 'temperature': 24, 'humidity': 502},
                         {'plant': 'd', 'hex_address': 34, 'temperature': 25, 'humidity': 503}]

        return cls.stringify_values(test_readings)

    @classmethod
    def stringify_square_brace_values(cls, values):
        """
        """

        def stringify_curly_brace_values(values: dict):
            srtingified_values = ",".join(f'"{key}":"{value}"' for key, value in values.items())
            # srtingified_values = ''
            # for key, value in values.items():
            #     srtingified_values += f'"{key}":"{value}"'
            return f'{{{srtingified_values}}}'

        return f'[{",".join(stringify_curly_brace_values(sensor_read) for sensor_read in values)}]'

    @classmethod
    def stringify_values(cls, readings: list):
        return cls.stringify_square_brace_values(values=readings)


if __name__ == '__main__':
    test_readings = [{'hex_address': 31, 'temperature': 22, 'humidity': 500},
                     {'hex_address': 32, 'temperature': 23, 'humidity': 501}]
    print(PMSHandler.stringify_values(test_readings))

"""
@author:    Krzysztof Brzozowski
@file:      pms_handler
@time:      18/03/2022
@desc:      STEMMA soil sensors (https://www.adafruit.com/product/4026) manager class.
"""
import time
import yaml

import board
from adafruit_seesaw.seesaw import Seesaw


class SensorManager:
    def __init__(self):
        self.i2c_bus = board.I2C()
        self.sensor_data = list()

        with open('config/config_sensor.yaml') as f:
            sensors_config = yaml.safe_load(f)

            for sensor_config in sensors_config:
                sensor_config.update({'temperature': None, 'humidity': None})
                self.sensor_data.append(sensor_config)

    def get_sensor_data(self, address):
        try:
            ss = Seesaw(self.i2c_bus, addr=address)
            return round(ss.get_temp(), 2), round(ss.moisture_read(), 2)

        except Exception as e:
            print(e)

    def get_all_data(self):
        """
        Get all values form the sensors (temperature, humidity)
        """
        for sensor in self.sensor_data:
            sensor['temperature'], sensor['humidity'] = self.get_sensor_data(sensor['hex_address'])

        return self.stringify_values(self.sensor_data)

    @staticmethod
    def stringify_square_brace_values(values):
        """
        """

        def stringify_curly_brace_values(values: dict):
            srtingified_values = ",".join(f'"{key}":"{value}"' for key, value in values.items())
            # srtingified_values = ''
            # for key, value in values.items():
            #     srtingified_values += f'"{key}":"{value}"'
            return f'{{{srtingified_values}}}'

        return f'[{",".join(stringify_curly_brace_values(sensor_read) for sensor_read in values)}]'

    def stringify_values(self, readings: list):
        return self.stringify_square_brace_values(values=readings)


if __name__ == '__main__':
    sensor_manager = SensorManager()
    while True:
        print(sensor_manager.get_all_data())
        time.sleep(5)

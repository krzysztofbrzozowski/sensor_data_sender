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
    i2c_bus = board.I2C()
    sensor_data = list()

    @classmethod
    def initialize_i2c(cls):
        with open('config/config_sensor.yaml') as f:
            sensors_config = yaml.safe_load(f)

            for sensor_config in sensors_config:
                sensor_config.update({'temperature': None, 'humidity': None})
                cls.sensor_data.append(sensor_config)

    @classmethod
    def read_sensor_values(cls, address):
        try:
            ss = Seesaw(cls.i2c_bus, addr=address)
            return round(ss.get_temp(), 2), round(ss.moisture_read(), 2)

        except Exception as e:
            print(e)

    @classmethod
    def get_sensor_data(cls):
        """
        Get all values form the sensors (temperature, humidity)
        """
        for sensor in cls.sensor_data:
            sensor['temperature'], sensor['humidity'] = cls.read_sensor_values(sensor['hex_address'])

        print(f'--i2c data {cls.sensor_data}')

    @classmethod
    def get_all_data(cls):
        print(f'Data I have {cls.stringify_values(cls.sensor_data)}')
        return cls.stringify_values(cls.sensor_data)

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

    @classmethod
    def stringify_values(cls, readings: list):
        return cls.stringify_square_brace_values(values=readings)


if __name__ == '__main__':
    SensorManager.initialize_i2c()

    while True:
        SensorManager.get_sensor_data()
        print(SensorManager.get_all_data())

        time.sleep(3)



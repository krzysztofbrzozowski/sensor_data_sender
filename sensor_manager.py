"""
@author:    Krzysztof Brzozowski
@file:      pms_handler
@time:      18/03/2022
@desc:      STEMMA soil sensors (https://www.adafruit.com/product/4026) manager class.
"""
import time
from typing import Optional, Any
import yaml
import board
from adafruit_seesaw.seesaw import Seesaw

# TODO if code is executed from main this import might be skipped
from logger import logger
import logging

logger = logging.getLogger('main_logger')


class SensorManager:
    """Class for handling all I2C sensors
    """
    i2c_bus = board.I2C()
    sensor_data = list()

    @classmethod
    def initialize_i2c(cls) -> None:
        """Initializes the base values of the data for the sensors included in YAML config

        :return: None
        """
        with open('config/config_sensor.yaml') as f:
            sensors_config = yaml.safe_load(f)

            for sensor_config in sensors_config:
                sensor_config.update({'temperature': None, 'humidity': None})
                cls.sensor_data.append(sensor_config)

    @classmethod
    def read_sensor_values(cls, address: int) -> Optional[tuple[Any, Any]]:
        """Gets data form sensors using I2C bus
        :param address:hex address of I2C sensor
        :type address: int

        :return: temperature and moisture read
        :rtype: tuple[float, float]
        """
        try:
            ss = Seesaw(cls.i2c_bus, addr=address)
            return round(ss.get_temp(), 2), round(ss.moisture_read(), 2)

        except Exception as e:
            logger.error('Issue occurred during reading from I2C sensor', exc_info=True)
            return None

    @classmethod
    def get_sensor_data(cls) -> None:
        """Gets all values form the sensors (temperature, humidity)

        :return: None
        """
        for sensor in cls.sensor_data:
            sensor['temperature'], sensor['humidity'] = cls.read_sensor_values(sensor['hex_address'])

        logger.debug(f'I2C output: Non-stringified data {cls.sensor_data}')

    @classmethod
    def get_all_data(cls) -> Optional[str]:
        """Gets all data read by i2c and stringifies it to be able to send using it IoT HAT

        :return: Stringified value of read data from i2c sensors
        :rtype: str
        """
        logger.debug(f'I2C output: Stringified data {cls.sensor_data}')
        try:
            return cls.stringify_values(cls.sensor_data)

        except TypeError as e:
            logger.error('Issue occurred during stringifying data from I2C sensor', exc_info=True)
            return None

    @staticmethod
    def stringify_square_brace_values(values_list: list) -> str:
        """Stringifies all items in list
        :param values_list: list of dictionaries with readings
        :type values_list: list

        :return: Sample data:  "[{'hex_address': 54, 'temperature': 21.45, 'humidity': 328}
                                {'hex_address': 55, 'temperature': 22.02, 'humidity': 425]"
        :rtype: str
        """
        def stringify_curly_brace_values(values_dict: dict):
            srtingified_values = ",".join(f'"{key}":"{value}"' for key, value in values_dict.items())
            return f'{{{srtingified_values}}}'

        return f'[{",".join(stringify_curly_brace_values(sensor_read) for sensor_read in values_list)}]'

    @classmethod
    def stringify_values(cls, readings: list) -> str:
        """Wrapper to stringify readings from sensors
        :param readings: list of dictionaries with sensors readings
        :type readings: list

        :return: Sample data:  "[{'hex_address': 54, 'temperature': 21.45, 'humidity': 328}
                                {'hex_address': 55, 'temperature': 22.02, 'humidity': 425]"
        :rtype: str
        """
        return cls.stringify_square_brace_values(values_list=readings)


if __name__ == '__main__':
    SensorManager.initialize_i2c()

    while True:
        SensorManager.get_sensor_data()
        print(SensorManager.get_all_data())

        time.sleep(3)



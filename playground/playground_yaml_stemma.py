"""
@author:    Krzysztof Brzozowski
@file:      playground_yaml
@time:      17/04/2022
@desc:      
"""
import time
import yaml
# import board
# from adafruit_seesaw.seesaw import Seesaw


def delay(time_sec: int):
    wait = time_sec * 10

    while wait:
        print('wait...')
        time.sleep(0.1)
        wait -= 1



class SensorManager:
    def __init__(self):
        """
        Initialize some values with empty readings
        [
            {'id': 'fcba1abf', 'plant': 'a', 'hex_address': 31,  read_interval: 60, 'temperature': None, 'humidity': None}
            ...
        ]

        """
        self.init_data()

    def init_data(self):
        self.sensor_values = list()

        with open('../config/config_sensor.yaml') as f:
            sensors = yaml.safe_load(f)
            for sensor in sensors:
                sensor.update({'temperature': None, 'humidity': None})
                self.sensor_values.append(sensor)

    # def get_reading_intervals(self):
    #     for sensor in self.sensor_values:
    #         interval = sensor['read_interval']

    def get_readings(self):
        for sensor in self.sensor_values:
            sensor['temperature'], sensor['humidity'] = self.get_sensor_data(sensor['hex_address'])

        for sensor in self.sensor_values:
            print(sensor)

    def get_sensor_data(self, address):
        # i2c_bus = board.I2C()
        # ss = Seesaw(i2c_bus, addr=address)
        #
        # humidity = ss.moisture_read()
        # temperature = ss.get_temp()

        # Test purposes
        temperature, humidity = 0, 0

        if address == 49:
            temperature, humidity = 18.0, 500
        if address == 50:
            temperature, humidity = 19.0, 502
        if address == 51:
            temperature, humidity = 28.0, 505
        if address == 52:
            temperature, humidity = 39.0, 506

        return temperature, humidity


if __name__ == '__main__':
    sensor_manager = SensorManager()
    while True:
        sensor_manager.get_readings()
        delay(5)


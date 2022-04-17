"""
@author:    Krzysztof Brzozowski
@file:      playground
@time:      11/04/2022
@desc:      Playground for running I2C devices directly from PC.
            https://www.adafruit.com/product/2264 is used
"""

import time
import board
from adafruit_seesaw.seesaw import Seesaw

import yaml

users = [{'name': 'John Doe', 'occupation': 'gardener'},
         {'name': 'Lucy Black', 'occupation': 'teacher'}]

with open('users.yaml', 'w+') as f:
    data = yaml.dump(users, f)

def read_values():
    i2c_bus = board.I2C()
    ss = Seesaw(i2c_bus, addr=0x36)

    moisture = ss.moisture_read()
    temp = ss.get_temp()

    print(f'Moisture: {moisture}, Temp: {temp}')


if __name__ == '__main__':
    while True:
        read_values()
        time.sleep(0.5)
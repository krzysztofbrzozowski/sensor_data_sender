"""
@author:    Krzysztof Brzozowski
@file:      playground_yaml
@time:      17/04/2022
@desc:      
"""
import yaml

test_readings = [{'plant': 'a', 'hex_address': 31, 'temperature': 22, 'humidity': 500},
                 {'plant': 'b', 'hex_address': 32, 'temperature': 23, 'humidity': 501},
                 {'plant': 'c', 'hex_address': 33, 'temperature': 24, 'humidity': 502},
                 {'plant': 'd', 'hex_address': 34, 'temperature': 25, 'humidity': 503}]


if __name__ == '__main__':
    # with open('test.yaml', 'w') as f:
    #     data = yaml.dump(test_readings, f, sort_keys=False)

    with open('../config/config_sensor.yaml') as f:
        sensors = yaml.safe_load(f)
        for x in sensors:
            x['hex_address']
            print(f'{x}')
import time

# import config
# import config_restricted
# import sysvar_manager
# from config_restricted import PHONE_NO
from dev_sim7000 import *
# # from dev_stemma import *
# from iot_mod import IoTMod as iot_mod
# from API_requests import APIRequests as api_requests
# from sysvar_manager import SysVarManager as SysVarMgr
from sensor_manager import SensorManager as SensorManager


if __name__ == '__main__':
    # TODO Fix initialize serial to be always on begin, why?
    # Initialize serial to communicate with SIM7000
    SIM7000.initialize_serial()

    # Configure APN
    SIM7000.initialize_apn()

    # Initialize HTTP requests
    SIM7000.initialize_requests()

    # Verify all settings are correct and try to fetch data
    current_time = SIM7000.send_get_request(url=f'{config.API_URL}/timesync')

    # average_temperature_data = SIM7000.send_get_request(url=f'{config.API_URL}/get-sensor-temperature/sensor_1/10')
    # print(average_temperature_data)
    #

    # payload = 'mac_address=00%3A00%3A00%3A00%3A00%3A00&temperature=11&humidity=22&pressure=777&adc=3.9'
    # SIM7000.send_post_request(url=f'{config.API_URL}', payload=payload, content='JSON')
    # SIM7000.send_sms(phone_no=config.PHONE_NO, msg=payload)

    # SOIL_SENSORS = 3
    # ss_sensors = {f'ss_sensor_{addr}': STEMMA(addr=addr) for addr in range(0x36, 0x36 + SOIL_SENSORS)}

    # # Post data to API using local connection
    # post_url = f'{config.API_URL}/post-pms-data'
    # payload_plant_readings = {
    #     'readings': [
    #         {'hex_address': 31, 'temperature': 21, 'humidity': 501},
    #         # {'hex_address': 32, 'temperature': 22, 'humidity': 502},
    #         # {'hex_address': 33, 'temperature': 23, 'humidity': 503}
    #     ],
    # }


    # payload = '[{"hex_address": 31, "temperature": 22, "humidity": 499}]'
    # api_requests.post(url=post_url, payload=payload_plant_readings['readings'])

    # Testing regular sensor request
    # payload_temp = '{"mac_address": "00:00:00:00:00:00","temperature": "22", "humidity": "500", "pressure": "888", "adc": "4.1"}'
    # SIM7000.send_post_request(url=f'{config.API_URL}',
    #                           # payload=payload_plant_readings['readings'],
    #                           payload=payload_temp,
    #                           auth_token=config_restricted.API_TOKEN,
    #                           content='JSON')

    # Testing pms data
    # payload_pms = '[{"hex_address": "01", "temperature": "50", "humidity": "100"},' \
    #               '{"hex_address": "02", "temperature": "50", "humidity": "101"}]'

    sensor_manager = SensorManager()
    while True:
        payload_pms = sensor_manager.get_all_data()
        print(payload_pms)
        time.sleep(5)

    # SIM7000.send_post_request(url=f'{config.API_URL}/post-pms-data',
    #                           # payload=payload_plant_readings['readings'],
    #                           payload=payload_pms,
    #                           auth_token=config_restricted.API_TOKEN,
    #                           content='JSON')


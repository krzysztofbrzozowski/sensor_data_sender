import config
import config_restricted
import sysvar_manager
from config_restricted import PHONE_NO
from dev_sim7000 import *
# from dev_stemma import *
from iot_mod import IoTMod as iot_mod
from API_requests import APIRequests as api_requests
from sysvar_manager import SysVarManager as SysVarMgr
# import asyncio


if __name__ == '__main__':
    # TODO Fix initialize serial to be always on begin, why?
    SIM7000.initialize_serial()
    # SIM7000.initialize_apn()
    # SIM7000.initialize_requests()
    #
    current_time = SIM7000.send_get_request(url=f'{config.API_URL}/timesync')
    # average_temperature_data = SIM7000.send_get_request(url=f'{config.API_URL}/get-sensor-temperature/sensor_1/10')
    # print(average_temperature_data)
    #

    # # # payload = 'mac_address=00%3A00%3A00%3A00%3A00%3A00&temperature=11&humidity=22&pressure=777&adc=3.9'
    # SIM7000.send_post_request(url=f'{config.API_URL}', payload=payload, content='JSON')
    # SIM7000.send_sms(phone_no=config.PHONE_NO, msg=payload)

    # SOIL_SENSORS = 3
    # ss_sensors = {f'ss_sensor_{addr}': STEMMA(addr=addr) for addr in range(0x36, 0x36 + SOIL_SENSORS)}

    # Post data to API using local connection
    post_url = f'{config.API_URL}/post-pms-data'
    payload_plant_readings = {
        'readings': [
            {'hex_address': 31, 'temperature': 21, 'humidity': 501},
            {'hex_address': 32, 'temperature': 22, 'humidity': 502},
            # {'hex_address': 33, 'temperature': 23, 'humidity': 503}
        ],
    }

    payload = '[{"hex_address": 31, "temperature": 22, "humidity": 499}]'

    # api_requests.post(url=post_url, payload=payload_plant_readings['readings'])
    SIM7000.send_post_request(url=f'{config.API_URL}',
                              # payload=payload_plant_readings['readings'],
                              payload=payload,
                              auth_token=config_restricted.API_TOKEN,
                              content='JSON')


    # SIM7000.send_sms(phone_no=PHONE_NO, message='Lorem Ipsum')

    pass

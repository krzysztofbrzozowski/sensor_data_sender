import config
# from dev_sim7000 import *
# from dev_stemma import *
from iot_mod import IoTMod as iot_mod
from API_requests import APIRequests as api_requests
# import asyncio


if __name__ == '__main__':
    iot_mod.initialize_serial()
    iot_mod.initialize_apn()

    current_time = iot_mod.send_GET_request(url=f'{config.API_URL}/timesync')
    print('GET MESSAGE', current_time)
    #
    # payload = '{"mac_address": "00:00:00:00:00:00", "temperature": "22", "humidity": "33", "pressure": "888", "adc": "4.1"}'
    # # payload = 'mac_address=00%3A00%3A00%3A00%3A00%3A00&temperature=11&humidity=22&pressure=777&adc=3.9'
    #
    # iot_mod.send_POST_request(url=f'{config.API_URL}', payload=payload, content='JSON')
    # SIM7000.send_sms(phone_no=config.PHONE_NO, msg=payload)

    # SOIL_SENSORS = 3
    # ss_sensors = {f'ss_sensor_{addr}': STEMMA(addr=addr) for addr in range(0x36, 0x36 + SOIL_SENSORS)}

    # Post data to API using local connection
    # post_url = f'{config.API_URL}/post-pms-data'
    #
    # payload_plant_readings = {
    #     'readings': [
    #         {'hex_address': 0x31, 'temperature': 21, 'humidity': 501},
    #         {'hex_address': 32, 'temperature': 22, 'humidity': 502},
    #         {'hex_address': 33, 'temperature': 23, 'humidity': 503}
    #     ],
    # }
    #
    # api_requests.post(url=post_url, payload=payload_plant_readings['readings'])

    pass

import config
from dev_sim7000 import *
from iot_mod import IoTMod as iot_mod


if __name__ == '__main__':
    iot_mod.initialize_serial()
    # iot_mod.initialize_apn()

    current_time = iot_mod.send_GET_request(url=f'{config.API_URL}/timesync')
    print('GET MESSAGE', current_time)

    payload = '{"mac_address": "00:00:00:00:00:00", "temperature": "22", "humidity": "33", "pressure": "888", "adc": "4.1"}'
    # payload = 'mac_address=00%3A00%3A00%3A00%3A00%3A00&temperature=11&humidity=22&pressure=777&adc=3.9'

    iot_mod.send_POST_request(url=f'{config.API_URL}', payload=payload, content='JSON')
    SIM7000.send_sms(phone_no=config.PHONE_NO, msg=payload)

    pass

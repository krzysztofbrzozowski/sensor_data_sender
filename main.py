import config
from dev_sim7000 import *
from iot_mod import IoTMod as iot_mod


if __name__ == '__main__':
    iot_mod.initialize_serial()
    # iot_mod.initialize_apn()

    current_time = iot_mod.send_GET_request(url=f'{config.API_URL}/timesync')
    print('GET MESSAGE', current_time)


    # message = {
    #     'date': datetime.now().strftime("%d.%m.%y - %H:%M:%S"),
    #     'text': 'test'
    # }
    # SIM7000.send_sms(phone_no='xxxxxxxxx', msg=message)

    pass

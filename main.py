import schedule

# import config
import config_restricted
from dev_sim7000 import *
# # from dev_stemma import *
# from iot_mod import IoTMod as iot_mod
# from API_requests import APIRequests as api_requests
# from sysvar_manager import SysVarManager as SysVarMgr
from sensor_manager import SensorManager as SensorManager
import time

from logger import logger
import logging

logger = logging.getLogger('main_logger')

if __name__ == '__main__':
    pass
    # TODO Fix initialize serial to be always on begin, why?
    # Initialize serial to communicate with SIM7000
    SIM7000.initialize_serial()

    # Configure APN
    SIM7000.initialize_apn()

    # Initialize HTTP requests
    SIM7000.initialize_requests()

    # Verify all settings are correct and try to fetch data
    current_time = SIM7000.send_get_request(url=f'{config.API_URL}/timesync')

    if len(current_time):
        logger.info(f'SIM7000 initialized, current time {current_time}')

    # Initialize I2C soil sensor
    SensorManager.initialize_i2c()
    SensorManager.get_sensor_data()

    # Test purposes
    # while True:
    #     payload = SensorManager.get_all_data()
    #
    # SIM7000.send_post_request(url=f'{config.API_URL}/post-pms-data',
    #                           payload=payload,
    #                           auth_token=config_restricted.API_TOKEN)
    #     time.sleep(5)

    # Schedule tasks
    schedule.every(20).minutes.do(SensorManager.get_sensor_data)
    schedule.every(60).minutes.do(
        lambda: SIM7000.send_post_request(url=f'{config.API_URL}/post-pms-data',
                                          payload=SensorManager.get_all_data(),
                                          auth_token=config_restricted.API_TOKEN))

    # Run now every scheduled task for test
    schedule.run_all()

    # Run every scheduled task
    while True:
        schedule.run_pending()
        time.sleep(1)


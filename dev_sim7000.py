import json
from datetime import datetime
import time
import sys
import platform

import config
from uart import *
from logger import logger


class SIM7000:
    _apn = config.APN
    _uart = UART(port=config.SERIAL_DARWIN if platform.system() == 'Darwin' else config.SERIAL_LINUX, baudrate=9600)

    @classmethod
    def initialize_serial(cls):
        """
        Fist initialization of UART communication
        It might occur that first time, loop will do few times before correct answer received
        """
        init_timeout = time.time() + 2.5

        cls._uart.start_serial_listen_thread()

        while not cls._uart.send_cmd('AT', 'OK', timeout=0.5) and time.time() < init_timeout:
            pass

        if time.time() >= init_timeout:
            return False
        return True

    @classmethod
    def terminate_serial(cls):
        """
        Terminate serial listening thread
        """
        cls._uart.stop_serial_listen_thread()

    # TODO - to remove?
    @classmethod
    def send_cmd(cls, cmd):
        cls._uart.send_cmd(cmd)

    # TODO - to remove?
    @classmethod
    def query_cmd(cls, cmd, timeout):
        return cls._uart.query_cmd(cmd, timeout=timeout)

    # TODO call this method only once automatically
    # TODO need to return something for iotmod config
    @classmethod
    def initialize_apn(cls):
        if not cls._apn:
            sys.exit('Set APN first')

        # Check if APN is set already
        # TODO add the while method as well like in intialize serial
        if not cls._uart.send_cmd(f'AT+CSTT?', expected=cls._apn, timeout=10):
            print('not initialized!')
            cls._uart.query_cmd(f'AT+CSTT="{cls._apn}"', expected='OK', timeout=2)      # Set APN
            cls._uart.query_cmd(f'AT+CIICR', expected='OK', timeout=10)                 # Bring up network

        time.sleep(5)

        cls._uart.query_cmd(f'AT+CIFSR', expected='.', timeout=10)                       # Get IP address

    @classmethod
    def initialize_requests(cls):
        cls._uart.query_cmd(f'AT+SAPBR=3,1,"APN","{cls._apn}"', expected='OK', timeout=1)  # Configure bearer profile 1
        cls._uart.query_cmd(f'AT+SAPBR=1,1', expected='OK', timeout=1)                     # To open bearer
        cls._uart.query_cmd(f'AT+HTTPINIT', expected='OK', timeout=1)
        cls._uart.query_cmd(f'AT+HTTPPARA="CID",1', expected='OK', timeout=1)              # Set parameters for HTTP session

    @classmethod
    def deinitialize_requests(cls):
        cls._uart.query_cmd(f'AT+HTTPTERM', expected='OK', timeout=1)           # Terminate HTTP service
        cls._uart.query_cmd(f'AT+SAPBR=0,1', expected='OK', timeout=1)          # To close bearer

    @classmethod
    def send_GET_request(cls, url: str, timeout: int = 10):
        """Send GET request with default timeout 10s
        :param: url: URL of the api containing exact address where get data from
        :param: timeout: when not receive any JSON data, timeout request
        :return: JSON data if any received, else None"""
        timeout = time.time() + timeout

        cls._uart.query_cmd(f'AT+HTTPPARA="URL","{url}"', expected='OK', timeout=1)         # Init HTTP service
        cls._uart.query_cmd(f'AT+HTTPACTION=0', expected='OK', timeout=1)                   # GET session start

        # TODO Can be removed, only while not loop leave?
        response = cls._uart.query_cmd(f'AT+HTTPREAD', expected='OK', timeout=1)
        while not any('{' and '}' in word for word in response) and time.time() < timeout:
            response = cls._uart.query_cmd(f'AT+HTTPREAD', expected='OK', timeout=1)
            time.sleep(1)

        try:
            return json.loads(response[response.index('OK') - 1])

        except Exception as e:
            print(e)
            return None

    @classmethod
    def send_POST_request(cls, url: str, payload: str, content: str = 'JSON'):
        cls._uart.query_cmd(f'AT+HTTPPARA="URL","{url}"', expected='OK', timeout=1)                 # Init HTTP service
        cls._uart.query_cmd(f'AT+HTTPPARA="CONTENT",'
                            f'{"application/json" if content == "JSON" else "application/x-www-form-urlencoded"}',
                            expected='OK', timeout=1)
        cls._uart.query_cmd(f'AT+HTTPDATA={len(payload)},2000', expected='OK', timeout=2)           # 1000 - max time for input the data
        cls._uart.query_data(f'{payload}', timeout=2)
        cls._uart.query_cmd(f'AT+HTTPACTION=1', expected='OK', timeout=2)

    @classmethod
    def send_sms(cls, phone_no, msg):
        cls._uart.query_cmd(f'AT+CMGF=1', 'OK', 2)
        cls._uart.query_cmd(f'AT+CNMI=2,1,0,0,0', 'OK', 2)
        cls._uart.query_cmd(f'AT+CMGS="{phone_no}"', 'OK', 2)
        cls._uart.query_cmd(f'{msg}', msg, None)
        cls._uart.send_byte(0x1A)

    @classmethod
    def send_byte(cls, byte):
        cls._uart.send_byte(byte)

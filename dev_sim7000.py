import json
from datetime import datetime
import requests
import time
import sys

import config
from uart import *


class SIM7000:
    _apn = config.APN
    # _uart = UART(port='/dev/ttyS0', baudrate=115200)
    _uart = UART(port='/dev/tty.usbserial-FT9JARY8', baudrate=115200)

    @classmethod
    def initialize_serial(cls):
        cls._uart.start_serial_listen_thread()
        while 'OK' not in cls._uart.query_cmd('AT', 'OK', timeout=0.1):
            cls._uart.query_cmd('AT', 'OK', timeout=0.1)
            time.sleep(0.1)

    @classmethod
    def send_cmd(cls, cmd):
        cls._uart.send_cmd(cmd)

    # TODO call this method only once automatically
    @classmethod
    def initialize_apn(cls):
        if not cls._apn:
            sys.exit('Set APN first')

        # Set APN
        assert 'OK' in cls._uart.query_cmd(f'AT+CSTT="{cls._apn}"', 'OK', timeout=2), 'APN not set'
        # Bring up network
        assert 'OK' in cls._uart.query_cmd(f'AT+CIICR', 'OK', timeout=10), 'Bringing up network failed'
        # Get IP address
        cls._uart.query_cmd(f'AT+CIFSR', '.', timeout=1), 'No IP address get'

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
        """Sending the GET request
        :param: url: URL of the api containing exact address where get data from
        :param: timeout: when not receive any JSON data, timeout request
        :return: JSON data if any received, else None"""
        timeout = time.time() + timeout

        cls._uart.query_cmd(f'AT+HTTPPARA="URL","{url}"', expected='OK', timeout=1)         # Init HTTP service
        cls._uart.query_cmd(f'AT+HTTPACTION=0', expected='OK', timeout=1)                   # GET session start

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

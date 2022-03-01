import json
from datetime import datetime
import time
import sys
import platform

import config
from uart import *
# from logger import logger
from sysvar_manager import SysVarManager


class SIM7000:
    _apn = config.APN
    _uart = UART(port=config.SERIAL_DARWIN if platform.system() == 'Darwin' else config.SERIAL_LINUX, baudrate=9600)

    @classmethod
    def initialize_serial(cls) -> bool:
        """
        Fist initialization of UART communication
        It might occur that first time, loop will do few times before correct answer received

        Returns
        -------
        bool
        """
        init_timeout = time.time() + 2.5

        cls._uart.start_serial_listen_thread()

        while not cls._uart.send_cmd(command='AT', response='OK', timeout=0.5) and time.time() < init_timeout:
            pass

        if time.time() >= init_timeout:
            Logger.log_error('UART communication not initialized')
            SysVarManager.set_sysvar(sysvar='serial_init', value='Error')
            return False

        return True

    @classmethod
    def terminate_serial(cls):
        """
        Terminate serial listening thread
        """
        cls._uart.stop_serial_listen_thread()

    @classmethod
    def initialize_apn(cls) -> bool:
        """
        Initialize APN if not set (LTE data handler)

        Returns
        -------
        bool
        """
        if not cls._apn:
            sys.exit('Set APN first')

        # Check if APN is set already
        if not cls._uart.send_cmd(command=f'AT+CSTT?', response=cls._apn, timeout=1):
            Logger.log_info(msg='APN not set in SIM7000 memory')
            cls._uart.send_cmd(command=f'AT+CSTT="{cls._apn}"', response='OK', timeout=2)      # Set APN
            cls._uart.send_cmd(command=f'AT+CIICR', response='OK', timeout=10)                 # Bring up network

        # time.sleep(5)

        # Get IP address
        if not cls._uart.send_cmd(f'AT+CIFSR', response='.', timeout=10):
            Logger.log_error('APN not initialized')
            SysVarManager.set_sysvar(sysvar='apn_init', value='Error')
            return False

        return True

    @classmethod
    def initialize_requests(cls) -> bool:
        """
        Initialize HTTP requests (LTE data handler)

        Returns
        -------
        bool
        """

        # Configure bearer profile 1
        cls._uart.send_cmd(command=f'AT+SAPBR=3,1,"APN","{cls._apn}"', response='OK', timeout=1)
        # To open bearer
        cls._uart.send_cmd(command=f'AT+SAPBR=1,1', response='OK', timeout=1)
        # Set parameters for HTTP session
        cls._uart.send_cmd(command=f'AT+HTTPINIT', response='OK', timeout=1)
        cls._uart.send_cmd(command=f'AT+HTTPPARA="CID",1', response='OK', timeout=1)

        return True

    @classmethod
    def terminate_requests(cls):
        """
        Terminate HTTP requests (LTE data handler)
        """
        # Terminate HTTP service
        cls._uart.send_cmd(command=f'AT+HTTPTERM', response='OK', timeout=1)
        # To close bearer
        cls._uart.send_cmd(command=f'AT+SAPBR=0,1', response='OK', timeout=1)

    @classmethod
    def send_GET_request(cls, url: str, timeout: int = 10):
        """Send GET request with default timeout 10s
        :param: url: URL of the api containing exact address where get data from
        :param: timeout: when not receive any JSON data, timeout request
        :return: JSON data if any received, else None"""
        timeout = time.time() + timeout

        cls._uart.send_cmd(f'AT+HTTPPARA="URL","{url}"', response='OK', timeout=1)         # Init HTTP service
        cls._uart.send_cmd(f'AT+HTTPACTION=0', response='OK', timeout=1)                   # GET session start

        # TODO Can be removed, only while not loop leave?
        response = cls._uart.query_cmd(f'AT+HTTPREAD', final_response='OK', timeout=1)
        while not any('{' and '}' in word for word in response) and time.time() < timeout:
            response = cls._uart.query_cmd(f'AT+HTTPREAD', final_response='OK', timeout=1)
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

    # TODO when there is long message sen as two messages?
    @classmethod
    def send_sms(cls, phone_no: str, message: str):
        """
        Send SMS message (SMS data handler)

        Returns
        -------
        bool
        """

        cls._uart.send_cmd(command=f'AT+CMGF=1', response='OK', timeout=1)
        cls._uart.send_cmd(command=f'AT+CNMI=2,1,0,0,0', response='OK', timeout=1)
        cls._uart.send_cmd(command=f'AT+CMGS="{phone_no}"', response='>', timeout=1)
        cls._uart.send_cmd(command=f'{message}', response=f'> {message}', timeout=10)

        if not cls._uart.send_byte(command=0x1A, response='OK', timeout=10):
            Logger.log_error('SMS not send')
            SysVarManager.set_sysvar(sysvar='sms_data_send', value='Error')
            return False

        return True

    @classmethod
    def send_byte(cls, byte):
        cls._uart.send_byte(byte)


    # TODO - to remove?
    @classmethod
    def send_cmd(cls, cmd):
        cls._uart.send_cmd(cmd)

    # TODO - to remove?
    @classmethod
    def query_cmd(cls, cmd, timeout):
        return cls._uart.query_cmd(cmd, timeout=timeout)

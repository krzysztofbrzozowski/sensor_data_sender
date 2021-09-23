import time
from datetime import datetime
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
    def configure_apn(cls):
        if not cls._apn:
            sys.exit('Set APN first')

        # Set APN
        assert 'OK' in cls._uart.query_cmd(f'AT+CSTT="{cls._apn}"', 'OK', timeout=2), 'APN not set'
        # Bring up network
        assert 'OK' in cls._uart.query_cmd(f'AT+CIICR', 'OK', timeout=10), 'Bringing up network failed'
        # Get IP address
        cls._uart.query_cmd(f'AT+CIFSR', '.', timeout=1), 'No IP address get'

    @classmethod
    def send_message(cls, phone_no, msg):
        cls._uart.query_cmd(f'AT+CMGF=1', 'OK', 2)
        cls._uart.query_cmd(f'AT+CNMI=2,1,0,0,0', 'OK', 2)
        cls._uart.query_cmd(f'AT+CMGS="{phone_no}"', 'OK', 2)
        cls._uart.query_cmd(f'{msg}', msg, None)
        cls._uart.send_byte(0x1A)

    @classmethod
    def send_byte(cls, byte):
        cls._uart.send_byte(byte)


if __name__ == '__main__':
    SIM7000.initialize_serial()
    SIM7000.configure_apn()

    message = {
        'date': datetime.now().strftime("%d.%m.%y - %H:%M:%S"),
        'text': 'test'
    }

    SIM7000.send_message(phone_no='xxxxxxxxx', msg=message)

    # print(message)
    pass

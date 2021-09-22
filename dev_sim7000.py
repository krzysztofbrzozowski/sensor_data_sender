import config
from uart import *

import sys


class SIM7000:
    _apn = config.APN
    _uart = UART(port='/dev/ttyS0', baudrate=115200)

    # TODO call this method only once automatically
    @classmethod
    def configure_apn(cls):
        if not cls._apn:
            sys.exit('Set APN first')

        # Set APN
        assert 'OK' in cls._uart.query_cmd(f'AT+CSTT="{cls._apn}"'), 'APN not set'
        # Bring up network
        assert 'OK' in cls._uart.query_cmd(f'AT+CIICR'), 'Bringing up network failed'

    @classmethod
    def test(cls):
        print('elo')
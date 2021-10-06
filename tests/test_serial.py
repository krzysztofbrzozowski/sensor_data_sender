import pytest


class TestSerial:
    @pytest.fixture(autouse=True)
    def setup_cleanup(self):
        self.exception = ''
        self.result = False

    def test_any_serial_device_is_connected(self):
        from uart_bckp import UART as UART
        import config

        try:
            uart = UART(port=config.SERIAL, baudrate=115200)
            if isinstance(uart, UART):
                self.result = True
        except BaseException as err:
            self.exception = err

        assert self.result is True, self.exception

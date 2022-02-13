import pytest
from platform import system


class TestSerial:
    @pytest.fixture(autouse=True)
    def setup_cleanup(self):
        self.exception = ''
        self.result = False

    def test_any_serial_device_is_connected(self):
        from uart import UART as UART
        import config

        try:
            uart = UART(port=config.SERIAL_DARWIN if system() == 'Darwin' else config.SERIAL_LINUX, baudrate=9600)

            if isinstance(uart, UART):
                self.result = True
        except BaseException as err:
            self.exception = err

        assert self.result is True, self.exception

    def test_send_cmd_function(self):
        pass

    def test_any_message_received_via_serial(self):
        from uart import UART as UART
        import config

        uart = UART(port=config.SERIAL_DARWIN if system() == 'Darwin' else config.SERIAL_LINUX, baudrate=9600)

        self.result = uart.send_cmd(cmd='AT', expected='OK', timeout=0.1)

        assert self.result is True

    def test_many_messages_received_via_serial(self):
        from uart import UART as UART
        import config

        uart = UART(port=config.SERIAL_DARWIN if system() == 'Darwin' else config.SERIAL_LINUX, baudrate=9600)

        received = [uart.send_cmd(cmd='AT', expected='OK', timeout=0.1) for _ in range(1000)]

        self.result = False if False in received else True

        assert self.result is True



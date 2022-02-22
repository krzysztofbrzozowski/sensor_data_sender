import time

import pytest
from platform import system

from uart import UART as UART
import config

import dev_sim7000

# class TestDevSim7000:
#     @pytest.fixture(autouse=True)
#     def setup_startup(self):
#         self.uart = UART(port=config.SERIAL_DARWIN if system() == 'Darwin' else config.SERIAL_LINUX, baudrate=9600)
#
#     @pytest.fixture(autouse=True)
#     def setup_cleanup(self):
#         self.exception = ''
#         self.result = False
#
#     @pytest.fixture
#     def mock_send_cmd(self, mocker):
#         return mocker.patch('cls._uart.send_cmd')
#
#
#     def test_any_serial_device_is_connected(self):
#         try:
#             if isinstance(self.uart, UART):
#                 self.result = True
#         except BaseException as err:
#             self.exception = err
#
#         assert self.result is True, self.exception
#
#     def test_initialize_serial_timeout_while_waiting_for_wrong_answer(self):
#         self.mock_send_cmd.return_value = False


class TestDevSim7000:
    @pytest.fixture(autouse=True)
    def setup_cleanup(self):
        self.result = False

    def test_initialize_serial_verify_timeout_while_waiting_for_wrong_answer(self, mocker):
        import time

        mocker.patch(
            'dev_sim7000.SIM7000._uart.send_cmd',
            return_value=False
        )

        time_start = time.time()
        dev_sim7000.SIM7000.initialize_serial()
        time_end = time.time() - time_start
        dev_sim7000.SIM7000.terminate_serial()

        self.result = True if abs(time_end) < 2.5 + 0.01 else False
        assert self.result is True

    def test_initialize_serial_verify_after_timeout_function_returns_false(self, mocker):
        mocker.patch(
            'dev_sim7000.SIM7000._uart.send_cmd',
            return_value=False
        )

        self.result = dev_sim7000.SIM7000.initialize_serial()
        dev_sim7000.SIM7000.terminate_serial()

        assert self.result is False

    def test_initialize_serial_verify_response_is_correct_function_returns_true(self):
        self.result = dev_sim7000.SIM7000.initialize_serial()

        dev_sim7000.SIM7000.terminate_serial()

        assert self.result is True

import time

import pytest
from platform import system

from uart import UART as UART
import config

import dev_sim7000


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
        # TODO sysvar has to be absolute path? Tests not passing because it can not find path sysvar/sysvar(.db)
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

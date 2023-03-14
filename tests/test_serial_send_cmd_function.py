import pytest
from platform import system

from drivers_low_level.uart import UART as UART
from config import config


class TestSerialSendCmdFunction:
    @pytest.fixture(autouse=True)
    def setup_startup(self):
        self.uart = UART(port=config.SERIAL_DARWIN if system() == 'Darwin' else config.SERIAL_LINUX, baudrate=9600)

    @pytest.fixture(autouse=True)
    def setup_cleanup(self):
        self.exception = ''
        self.result = False

    # Initialization tests
    def test_any_serial_device_is_connected(self):
        try:
            if isinstance(self.uart, UART):
                self.result = True
        except BaseException as err:
            self.exception = err

        assert self.result is True, self.exception

    def test_killing_thread(self):
        self.uart.start_serial_listen_thread()
        self.uart.stop_serial_listen_thread()
        assert True

    # Method send_cmd tests
    def test_send_cmd_verify_no_command_to_send_returns_false(self):
        self.uart.start_serial_listen_thread()
        self.result = self.uart.send_cmd(command=None, response=None, timeout=None)
        self.uart.stop_serial_listen_thread()

        assert self.result is False

    def test_send_cmd_verify_response_not_in_answer_returns_false(self):
        self.uart.start_serial_listen_thread()
        self.result = self.uart.send_cmd(command='AT', response='not_in_answer', timeout=1)
        self.uart.stop_serial_listen_thread()

        assert self.result is False

    def test_send_cmd_verify_timeout_while_waiting_for_wrong_response(self):
        import time

        self.uart.start_serial_listen_thread()
        time_start = time.time()
        self.uart.send_cmd(command='AT', response='not_in_answer', timeout=1)
        time_end = time.time() - time_start
        self.uart.stop_serial_listen_thread()

        self.result = True if abs(time_end) < 1 + config.MESSAGE_PROPAGATION_TIME + 0.01 else False
        assert self.result is True

    def test_send_cmd_verify_expected_response_is_none_returns_true(self):
        self.uart.start_serial_listen_thread()
        self.result = self.uart.send_cmd(command='AT', response=None, timeout=1)
        self.uart.stop_serial_listen_thread()

        assert self.result is True

    def test_send_cmd_verify_timeout_while_waiting_for_none_response(self):
        import time

        self.uart.start_serial_listen_thread()
        time_start = time.time()
        self.uart.send_cmd(command='AT', response=None, timeout=1)
        time_end = time.time() - time_start
        self.uart.stop_serial_listen_thread()

        self.result = True if abs(time_end) < 1 + config.MESSAGE_PROPAGATION_TIME + 0.01 else False
        assert self.result is True

    def test_send_cmd_verify_default_timeout_while_waiting_for_none_response(self):
        import time

        self.uart.start_serial_listen_thread()
        time_start = time.time()
        self.uart.send_cmd(command='AT', response=None)
        time_end = time.time() - time_start
        self.uart.stop_serial_listen_thread()

        self.result = True if abs(time_end) < 2.0 + config.MESSAGE_PROPAGATION_TIME + 0.01 else False
        assert self.result is True

    def test_send_cmd_verify_that_finding_response_returns_true(self):
        self.uart.start_serial_listen_thread()
        self.result = self.uart.send_cmd(command='AT', response='OK', timeout=1)
        self.uart.stop_serial_listen_thread()

        assert self.result is True

    def test_send_cmd_verify_timeout_not_working_if_find_correct_response(self):
        import time

        self.uart.start_serial_listen_thread()
        time_start = time.time()
        self.uart.send_cmd(command='AT', response='OK', timeout=1)
        time_end = time.time() - time_start
        self.uart.stop_serial_listen_thread()

        # 0.5 to be sure that expecting answer is detected much faster than timeout
        self.result = True if abs(time_end) < 0.5 + config.MESSAGE_PROPAGATION_TIME else False
        assert self.result is True

    def test_send_cmd_verify_rx_buffer_clearing_after_message(self):
        self.uart.start_serial_listen_thread()
        result_return_msg = self.uart.send_cmd(command='AT', response='OK', timeout=1)
        self.uart.stop_serial_listen_thread()

        assert result_return_msg is True

        result_rx_buffer_is_empty = True if not len(self.uart.get_rx_buf()) else False
        assert result_rx_buffer_is_empty is True

    def test_send_cmd_verify_10_responses_received_via_serial(self):
        self.uart.start_serial_listen_thread()

        self.result = True
        for _ in range(10):
            if not self.uart.send_cmd(command='AT', response='OK', timeout=1):
                self.result = False
                break

        self.uart.stop_serial_listen_thread()

        assert self.result is True

    def test_send_cmd_verify_100_responses_received_via_serial(self):
        self.uart.start_serial_listen_thread()

        self.result = True
        for _ in range(100):
            if not self.uart.send_cmd(command='AT', response='OK', timeout=1):
                self.result = False
                break

        self.uart.stop_serial_listen_thread()

        assert self.result is True



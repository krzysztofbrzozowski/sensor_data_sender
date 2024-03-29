import pytest
from platform import system

from drivers_low_level.uart import UART as UART
from config import config


class TestSerialQueryCmdFunction:
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

    # Method query_cmd tests
    def test_query_cmd_verify_no_command_to_send_returns_empty_list(self):
        self.uart.start_serial_listen_thread()
        rx = self.uart.query_cmd(command=None, final_response=None, timeout=None)
        self.uart.stop_serial_listen_thread()

        self.result = False if not len(rx) else True
        assert self.result is False

    def test_query_cmd_verify_expected_final_response_not_in_answer_returns_empty_list(self):
        self.uart.start_serial_listen_thread()
        rx = self.uart.query_cmd(command='ATI', final_response='not_in_answer', timeout=1)
        self.uart.stop_serial_listen_thread()

        self.result = False if not len(rx) else True
        assert self.result is False

    def test_query_cmd_verify_timeout_while_waiting_for_wrong_final_response(self):
        import time

        self.uart.start_serial_listen_thread()
        time_start = time.time()
        self.uart.query_cmd(command='ATI', final_response='not_in_answer', timeout=1)
        time_end = time.time() - time_start
        self.uart.stop_serial_listen_thread()

        # TODO Add variable timeout depending on platform e.g. RPi Zero, RPi 3B etc
        self.result = True if abs(time_end) < 1 + config.MESSAGE_PROPAGATION_TIME + 0.3 else False
        assert self.result is True

    def test_query_cmd_verify_expected_final_response_none_returns_rx_buffer(self):
        self.uart.start_serial_listen_thread()
        rx = self.uart.query_cmd(command='ATI', final_response=None, timeout=1)
        self.uart.stop_serial_listen_thread()

        self.result = True if 'SIM7000E R1351' in rx else False
        assert self.result is True

    def test_query_cmd_verify_timeout_while_waiting_for_none_final_response(self):
        import time

        self.uart.start_serial_listen_thread()
        time_start = time.time()
        self.uart.query_cmd(command='ATI', final_response=None, timeout=1)
        time_end = time.time() - time_start
        self.uart.stop_serial_listen_thread()

        self.result = True if abs(time_end) < 1 + config.MESSAGE_PROPAGATION_TIME + 0.01 else False
        assert self.result is True

    def test_query_cmd_verify_default_timeout_while_waiting_for_none_final_response(self):
        import time

        self.uart.start_serial_listen_thread()
        time_start = time.time()
        self.uart.query_cmd(command='ATI', final_response=None)
        time_end = time.time() - time_start
        self.uart.stop_serial_listen_thread()

        self.result = True if abs(time_end) < 2.0 + config.MESSAGE_PROPAGATION_TIME + 0.01 else False
        assert self.result is True

    def test_query_cmd_verify_that_finding_response_returns_rx_buffer(self):
        self.uart.start_serial_listen_thread()
        rx = self.uart.query_cmd(command='ATI', final_response='OK', timeout=1)
        self.uart.stop_serial_listen_thread()

        self.result = True if 'SIM7000E R1351' in rx else False
        assert self.result is True

    def test_query_cmd_verify_timeout_not_working_if_find_correct_final_response(self):
        import time

        self.uart.start_serial_listen_thread()
        time_start = time.time()
        self.uart.query_cmd(command='ATI', final_response='OK', timeout=1)
        time_end = time.time() - time_start
        self.uart.stop_serial_listen_thread()

        # 0.5 to be sure that expecting answer is detected much faster than timeout
        self.result = True if abs(time_end) < 0.5 + config.MESSAGE_PROPAGATION_TIME else False
        assert self.result is True

    def test_query_cmd_verify_rx_buffer_clearing_after_message(self):
        self.uart.start_serial_listen_thread()
        rx = self.uart.query_cmd(command='ATI', final_response='OK', timeout=1)
        self.uart.stop_serial_listen_thread()

        result_return_msg = True if len(rx) else False
        assert result_return_msg is True

        result_rx_buffer_is_empty = True if not len(self.uart.get_rx_buf()) else False
        assert result_rx_buffer_is_empty is True

    def test_query_cmd_verify_10_responses_received_via_serial(self):
        self.uart.start_serial_listen_thread()

        self.result = True
        for _ in range(10):
            if 'SIM7000E R1351' not in self.uart.query_cmd(command='ATI', final_response='OK', timeout=1):
                self.result = False
                break

        self.uart.stop_serial_listen_thread()

        assert self.result is True

    def test_query_cmd_verify_100_responses_received_via_serial(self):
        self.uart.start_serial_listen_thread()

        self.result = True
        for _ in range(100):
            if 'SIM7000E R1351' not in self.uart.query_cmd(command='ATI', final_response='OK', timeout=1):
                self.result = False
                break

        self.uart.stop_serial_listen_thread()

        assert self.result is True




import pytest

from platform import system

from uart import UART as UART
import config


class TestSerial:
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
    def test_send_cmd_no_command_to_send_returns_false(self):
        self.uart.start_serial_listen_thread()
        self.result = self.uart.send_cmd(command=None, expected=None, timeout=None)
        self.uart.stop_serial_listen_thread()

        assert self.result is False

    def test_send_cmd_expected_not_in_answer_returns_false(self):
        self.uart.start_serial_listen_thread()
        self.result = self.uart.send_cmd(command='AT', expected='not_in_answer', timeout=1)
        self.uart.stop_serial_listen_thread()

        assert self.result is False

    def test_send_cmd_verify_timeout_while_waiting_for_wrong_answer(self):
        import time

        self.uart.start_serial_listen_thread()
        time_start = time.time()
        self.uart.send_cmd(command='AT', expected='not_in_answer', timeout=1)
        time_end = time.time() - time_start
        self.uart.stop_serial_listen_thread()

        self.result = True if abs(time_end) < 1 + config.MESSAGE_PROPAGATION_TIME + 0.01 else False
        assert self.result is True

    def test_send_cmd_returning_true_if_everything_ok(self):
        self.uart.start_serial_listen_thread()
        self.result = self.uart.send_cmd(command='AT', expected='OK', timeout=1)
        self.uart.stop_serial_listen_thread()

        assert self.result is True

    def test_any_message_received_via_serial(self):
        self.uart.start_serial_listen_thread()

        self.result = self.uart.send_cmd(command='AT', expected='OK', timeout=1)

        self.uart.stop_serial_listen_thread()
        assert self.result is True

    # def test_many_messages_received_via_serial(self):
    #     # Initialize serial
    #     uart.start_serial_listen_thread()
    #
    #     received = [uart.send_cmd(command='AT', expected='OK', timeout=0.1) for _ in range(10)]
    #
    #     # Deinitialize serial
    #     uart.stop_serial_listen_thread()
    #     self.result = False if False in received else True
    #     assert self.result is True



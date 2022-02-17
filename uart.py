import threading
import time
import serial
import config

from logger.logger import Logger


class UART:
    def __init__(self, port: str, baudrate: int):
        self._serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self._rx_buf = []
        self._serial_thread = None
        self._stop_event = threading.Event()

    def get_rx_buf(self):
        return self._rx_buf

    def set_rx_buf(self, arg):
        self._rx_buf = arg

    # def send_cmd(self, cmd):
    #     self._serial.write(f'{cmd}\r\n'.encode('ascii'))
    #     time.sleep(0.01)
    #     self.set_rx_buf([])

    def send_byte(self, cmd):
        self._serial.write(serial.to_bytes([cmd]))

    def send_cmd(self, command: str = None, expected: str = None, timeout: float = 2.0) -> bool:
        """
        Send command and await for expected answer if defined, else wait for timeout

        Parameters
        ----------
        command: str
            Command send via UART
        expected: str
            Expected answer to find in serial output
        timeout: float
            Timeout for expecting answer or only wait time, default is 2.0

        Returns
        -------
        bool
            True if expected answer occurred else False
        """

        # Exit function with warning if no command to send defined

        try:
            if not command:
                Logger.log_warning(f'No command to send defined')
                return False

            Logger.log_info(f'Sent command: {command}; Expecting in answer: {expected}; Timeout: {timeout};')

            self._serial.write(f'{command}\r\n'.encode('ascii'))
            time.sleep(config.MESSAGE_PROPAGATION_TIME)

            timeout = time.time() + timeout

            # Wait for occurrence of expected string, if not return False
            if expected and timeout:
                while not any(expected in s for s in self.get_rx_buf()) and time.time() < timeout:
                    pass

                if time.time() >= timeout:
                    Logger.log_warning(f'Timeout occurred while sending: {command} and waiting for: {expected}')
                    return False

                # If expected argument is present, return True
                if any(expected in s for s in self.get_rx_buf()):
                    return True
                return False

            # If only timeout is defined, wait max time to go further
            if not expected and timeout:
                while time.time() < timeout:
                    pass
                return True

        # Before exit, always clear rx_buf
        finally:
            self.set_rx_buf([])

    def query_cmd(self, cmd, expected=None, timeout=None):
        self._serial.write(f'{cmd}\r\n'.encode('ascii'))
        Logger.log_info(f'Sent command: {cmd}; Expecting in answer: {expected}; Timeout: {timeout};')

        time.sleep(0.2)

        timeout = time.time() + timeout if timeout else None

        # Wait for occurrence of expected string
        if expected and timeout:
            while not any(expected in s for s in self.get_rx_buf()) and time.time() < timeout:
                pass

            if time.time() >= timeout:
                Logger.log_warning(f'Timeout occurred while: {cmd}')

        if not expected and timeout:
            while time.time() < timeout:
                pass

            if time.time() >= timeout:
                Logger.log_warning(f'Timeout occurred while: {cmd}')

        local_rx_buf = self.get_rx_buf()
        self.set_rx_buf([])

        return local_rx_buf

    def query_data(self, data, expected=None, timeout=None):
        timeout = time.time() + timeout if timeout else None

        self._serial.write(f'{data}\r\n'.encode('ascii'))
        time.sleep(0.05)

        if expected and timeout:
            while expected not in self.get_rx_buf() and time.time() < timeout:
            # while not any(expected in word for word in self.get_rx_buf()) and time.time() < timeout:
                pass
        if timeout:
            while time.time() < timeout:
                pass

        tmp = self.get_rx_buf()
        self.set_rx_buf([])
        return tmp

    # def serial_listener(self):
    #     while not self._stop_event.is_set():
    #         read = self._serial.readline()
    #         if read != bytes():
    #             print(read)
    #             read = read.strip().decode()
    #             self._rx_buf.append(read)
    #
    #             if config.DEBUG:
    #                 print(self._rx_buf)

    def serial_listener(self):
        while not self._stop_event.is_set():
            read = self._serial.readline()
            if read != bytes():
                try:
                    read = read.strip().decode()
                    self._rx_buf.append(read)
                except BaseException as e:
                    Logger.log_error(e)

                Logger.log_debug(f'Serial output: {self._rx_buf}')
                # time.sleep(0.01)

    def start_serial_listen_thread(self):
        if not self._serial.isOpen():
            self._serial.open()
        self._serial_thread = threading.Thread(target=self.serial_listener, args=())
        self._serial_thread.start()

    def stop_serial_listen_thread(self):
        self._stop_event.set()
        self._serial_thread.join()

    def clear_all(self):
        self._serial.flushInput()
        self._serial.flushOutput()
        self._serial.flush()






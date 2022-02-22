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

    def send_cmd(self, command: str = None, response: str = None, timeout: float = 2.0) -> bool:
        """
        Send command and await for expected answer if defined, else wait for timeout

        Parameters
        ----------
        command: str
            Command send via UART
        response: str
            Expected response to find in serial output
        timeout: float
            Timeout for expecting answer or only wait time, default is 2.0

        Returns
        -------
        bool
            True if expected answer occurred else False
        """

        try:
            # Exit function with warning if no command to send defined
            if not command:
                Logger.log_warning(f'No command to send defined')
                return False

            Logger.log_info(f'Sent command: {command};'
                            f'Expecting response in answer: {response};'
                            f'Timeout: {timeout};')

            self._serial.write(f'{command}\r\n'.encode('ascii'))
            time.sleep(config.MESSAGE_PROPAGATION_TIME)

            timeout = time.time() + timeout

            # Wait for occurrence of expected string, if not return False
            if response and timeout:
                while not any(response in s for s in self.get_rx_buf()) and time.time() < timeout:
                    pass

                if time.time() >= timeout:
                    Logger.log_warning(f'Timeout occurred while sending: {command} and waiting for: {response}')
                    return False

                # If response argument is present, return True
                if any(response in s for s in self.get_rx_buf()):
                    return True
                return False

            # If only timeout is defined, wait max time to go further
            if not response and timeout:
                while time.time() < timeout:
                    pass
                return True

        # Before exit, always clear rx_buf
        finally:
            self.set_rx_buf([])

    def query_cmd(self, command: str = None, final_response: str = None, timeout: float = 2.0) -> list:
        """
        Send command and await for final_response if defined, else wait for timeout

        Parameters
        ----------
        command: str
            Command send via UART
        final_response: str
            Expected final response to find in serial output
        timeout: float
            Timeout for expecting answer or only wait time, default is 2.0

        Returns
        -------
        list
            List of returned values if final response occurred else empty list
        """

        try:
            # Exit function with warning if no command to send defined
            if not command:
                Logger.log_warning(f'No command to send defined')
                return []

            Logger.log_info(f'Sent command: {command};'
                            f'Expecting final response in answer: {final_response}; '
                            f'Timeout: {timeout};')

            self._serial.write(f'{command}\r\n'.encode('ascii'))
            time.sleep(config.MESSAGE_PROPAGATION_TIME)

            timeout = time.time() + timeout

            # Wait for occurrence of expected string, if not return empty list
            if final_response and timeout:
                while not any(final_response in s for s in self.get_rx_buf()) and time.time() < timeout:
                    pass

                if time.time() >= timeout:
                    Logger.log_warning(f'Timeout occurred while sending: {command} and waiting for: {final_response}')
                    return []

                # If final response argument is present, return True
                if any(final_response in s for s in self.get_rx_buf()):
                    return self.get_rx_buf()
                return []

            # If only timeout is defined, wait max time to go further
            if not final_response and timeout:
                while time.time() < timeout:
                    pass
                return self.get_rx_buf()

        # Before exit, always clear rx_buf
        finally:
            self.set_rx_buf([])

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
        """
        Main serial listener function
        """

        while not self._stop_event.is_set():
            read = self._serial.readline()
            if read != bytes():
                try:
                    read = read.strip().decode()
                    self._rx_buf.append(read)
                except BaseException as e:
                    Logger.log_error(e)

                Logger.log_debug(f'Serial output: {self._rx_buf}')

    def start_serial_listen_thread(self):
        """
        Run serial listener in another thread
        """

        if self._stop_event.is_set():
            self._stop_event.clear()

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






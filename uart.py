import threading
import time
import serial
import config


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

    def send_cmd(self, cmd, expected=None, timeout=None):
        """Send cmd and await for expected answer
        :param: cmd: command to send
        :param: expected: expected answer
        :param: timeout: timeout
        :return: True if expected answer occurred else False"""

        timeout = time.time() + timeout if timeout else None

        self._serial.write(f'{cmd}\r\n'.encode('ascii'))
        time.sleep(0.1)

        # Wait for occurrence of expected string
        if expected and timeout:
            while not any(expected in s for s in self.get_rx_buf()) and time.time() < timeout:
                pass

        if timeout:
            while time.time() < timeout:
                pass

        # If expected argument is present, return True or False only
        if expected:
            if any(expected in s for s in self.get_rx_buf()):
                return True
            return False

    def query_cmd(self, cmd, expected=None, timeout=None):
        timeout = time.time() + timeout if timeout else None

        self._serial.write(f'{cmd}\r\n'.encode('ascii'))
        time.sleep(0.1)

        # Wait for occurrence of expected string
        if expected and timeout:
            while not any(expected in s for s in self.get_rx_buf()) and time.time() < timeout:
                pass

        if timeout:
            while time.time() < timeout:
                pass

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
                    if config.DEBUG:
                        print(e)

                if config.DEBUG:
                    print(self._rx_buf)

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






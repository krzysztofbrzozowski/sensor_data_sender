import time
import serial
from threading import Thread


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

    def get_rx_buf(self):
        return self._rx_buf

    def set_rx_buf(self, arg):
        self._rx_buf = arg

    def send_cmd(self, cmd):
        self._serial.write(f'{cmd}\r\n'.encode('ascii'))
        time.sleep(0.01)
        self.set_rx_buf([])

    def send_byte(self, cmd):
        self._serial.write(serial.to_bytes([cmd]))

    def query_cmd(self, cmd, expected=None, timeout=None):
        timeout = time.time() + timeout if timeout else None

        self._serial.write(f'{cmd}\r\n'.encode('ascii'))
        time.sleep(0.1)

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

    # def query_cmd(self, cmd, expected, timeout):
    #     self._serial.write(f'{cmd}\r\n'.encode('ascii'))
    #     time.sleep(0.1)
    #     tmp = self.get_rx_buf()
    #     self.set_rx_buf([])
    #     return tmp

    def serial_listener(self):
        while True:
            read = self._serial.readline()
            if read != bytes():
                read = read.strip().decode()
                self._rx_buf.append(read)
                print(self._rx_buf)

    def start_serial_listen_thread(self):
        if not self._serial.isOpen():
            self._serial.open()
        Thread(target=self.serial_listener, args=()).start()

    def clear_all(self):
        self._serial.flushInput()
        self._serial.flushOutput()
        self._serial.flush()






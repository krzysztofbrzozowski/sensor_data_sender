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

    def set_rx_buf(self, *arg):
        self._rx_buf = arg

    def send_cmd(self, cmd):
        self._serial.write(f'{cmd}\r\n'.encode('ascii'))
        time.sleep(0.05)

    def query_cmd(self, cmd):
        self._serial.write(f'{cmd}\r\n'.encode('ascii'))
        time.sleep(0.05)
        tmp = self.get_rx_buf()
        self.set_rx_buf([])
        return tmp


    def serial_listener(self):
        while True:
            read = self._serial.read()
            if read != bytes() and read != b'\x00':
                self._rx_buf.append(read)

    def start_serial_listen_thread(self):
        if not self._serial.isOpen():
            self._serial.open()
        Thread(target=self.serial_listener, args=()).start()





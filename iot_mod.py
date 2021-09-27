from dev_sim7000 import *


class IoTMod:
    _initialize_serial = False
    _initialize_apn = False

    _initialize_requests = False
    _initialize_bearer = False

    @classmethod
    def initialize_serial(cls):
        SIM7000.initialize_serial()
        cls._initialize_serial = True

    @classmethod
    def initialize_apn(cls):
        SIM7000.initialize_apn()
        cls._initialize_apn = True

    @classmethod
    def initialize_requests(cls):
        SIM7000.initialize_requests()
        cls._initialize_requests = True

    @classmethod
    def send_GET_request(cls, url: str):
        if not cls._initialize_requests:
            cls.initialize_requests()

        response = SIM7000.send_GET_request(url=url)
        return response

    @classmethod
    def send_POST_request(cls, url: str, data: str):
        if not cls._initialize_requests:
            cls.initialize_requests()

        response = SIM7000.send_POST_request(url=url, data=data)
        return response



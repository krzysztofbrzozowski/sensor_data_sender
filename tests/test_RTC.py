import pytest


class TestRTC:
    def test_get_local_date(self):
        """Get only the local date"""
        from datetime import datetime

        try:
            now = datetime.now()
            result = [int(current_x) for current_x in now.strftime("%d-%m-%y").split('-')]
        except ValueError:
            pass

        assert result[0] > 0, 'Read current date failed'

    def test_get_server_date(self):
        """Get the date form server using IoT Hat"""



        iot_mod.initialize_apn()

        current_time = iot_mod.send_GET_request(url=f'{config.API_URL}/timesync')

        assert current_time


    def test_get_any_temperature_value(self):
        pass
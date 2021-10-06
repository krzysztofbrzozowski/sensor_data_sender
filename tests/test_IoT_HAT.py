import time

import pytest


class TestIoTHAT:
    @pytest.fixture(autouse=True)
    def setup_cleanup(self):
        self.exception = ''
        self.result = False

    def test_any_response_from_iot_hat(self):
        from dev_sim7000 import SIM7000

        SIM7000.initialize_serial()

        if 'OK' in SIM7000.query_cmd('AT', timeout=1):
            self.result = True

        SIM7000.deinitialize_serial()

        assert self.result is True




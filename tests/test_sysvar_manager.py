"""
@author:    Krzysztof Brzozowski
@file:      test_sysvar_manager
@time:      01/03/2022
@desc:      
"""

import pytest
from drivers_high_level.sysvar_manager import SysVarManager, init_sysvar_dict


class TestSysVarManager:
    @pytest.fixture(autouse=True)
    def setup_setup(self):
        self.test_database = 'test_database'

    @pytest.fixture(autouse=True)
    def setup_cleanup(self):
        self.result = False

    def test_init_sysvar_db_verify_database_existing(self):
        import os

        SysVarManager.SYSVAR_DB = self.test_database
        SysVarManager.init_sysvar_db()
        self.result = True if os.path.exists(f'{SysVarManager.SYSVAR_DB}.db') else False

        assert self.result is True

    def test_init_sysvar_db_verify_database_has_all_dictionary_records_and_remove_db(self):
        import os

        SysVarManager.SYSVAR_DB = self.test_database

        for k, v in init_sysvar_dict.items():
            if not SysVarManager.get_sysvar(sysvar=k) == v:
                self.result = False
                continue

            self.result = True

        if os.path.exists(f'{SysVarManager.SYSVAR_DB}.db'):
            os.remove(f'{SysVarManager.SYSVAR_DB}.db')

        assert self.result is True





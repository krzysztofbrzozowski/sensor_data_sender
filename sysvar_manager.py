"""
@author:    Krzysztof Brzozowski
@file:      system_variables
@time:      01/03/2022
@desc:      Class SysVarManager handles persistence variables stored on local drive
"""

import shelve

init_sysvar_dict = {
    'serial_init':  None,
    'apn_init':     None,
}


class SysVarManager:
    SYSVAR_DB = 'sysvar/sysvar'

    @classmethod
    def set_sysvar(cls, sysvar: str, value):
        sh = shelve.open(filename=cls.SYSVAR_DB, flag='c')
        sh[sysvar] = value
        sh.close()

    @classmethod
    def get_sysvar(cls, sysvar: str):
        sh = shelve.open(filename=cls.SYSVAR_DB, flag='r')
        sysvar_value = sh[sysvar]
        sh.close()
        return sysvar_value

    @classmethod
    def init_sysvar_db(cls):
        for k, v in init_sysvar_dict.items():
            cls.set_sysvar(sysvar=k, value=v)

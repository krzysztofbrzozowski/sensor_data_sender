"""
Class SysVarManager handles persistence variables stored on local drive
"""
import shelve


class SysVarManager:
    SYSVAR_DB = 'sysvar/sysvar.db'

    @classmethod
    def set_sysvar(cls, sysvar: str, value):
        sh = shelve.open(cls.SYSVAR_DB)
        sh[sysvar] = value
        sh.close()

    @classmethod
    def get_sysvar(cls, sysvar: str):
        sh = shelve.open(cls.SYSVAR_DB)
        sysvar_value = sh[sysvar]
        sh.close()
        return sysvar_value

    # TODO get sysvars form list
    @classmethod
    def init_sysvar_db(cls):
        cls.set_sysvar('uart_init', 'None')


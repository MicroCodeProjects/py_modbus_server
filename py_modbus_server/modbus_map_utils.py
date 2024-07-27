from .exceptions import (
    InvalidSlaveError,
    InvalidRegisterTypeError,
    InvalidAddressError,
    InvalidNameError,
)


class ModbusMapValidator:

    def __init__(self, modbus_map):

        self.modbus_map = modbus_map

    def check_slave_id(self, slave_id: int):

        if slave_id not in self.modbus_map:
            raise InvalidSlaveError(slave_id)

    def check_register_type(self, slave_id: int, register_type: str):

        self.check_slave_id(slave_id)

        if register_type not in self.modbus_map[slave_id]:
            raise InvalidRegisterTypeError(register_type)

    def check_mb_variable_name(self, slave_id: int, register_type: str, mb_variable_name: str):

        self.check_register_type(slave_id, register_type)

        if mb_variable_name not in self.modbus_map[slave_id][register_type]:
            raise InvalidNameError(mb_variable_name)

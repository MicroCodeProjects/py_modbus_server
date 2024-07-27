import asyncio
import threading

from pymodbus.datastore import ModbusSlaveContext, ModbusSparseDataBlock, ModbusServerContext
from pymodbus.server import ModbusTcpServer as _ModbusTcpServer

from ._auxiliary_functions import is_type
from ._types import ModbusMapTypeSingleSlave, ModbusMapTypeMultipleSlaves
from .modbus_map_utils import ModbusMapValidator


class ModbusTcpServer:

    def __init__(
            self,
            modbus_map: ModbusMapTypeMultipleSlaves | ModbusMapTypeSingleSlave,
            host: str = "127.0.0.1",
            port: int = 502,
            timeout: float = 0.5,
    ):

        if is_type(modbus_map, ModbusMapTypeSingleSlave):
            modbus_map = {0: modbus_map}
            self._single = True
        else:
            self._single = False

        self.modbus_map: ModbusMapTypeMultipleSlaves = modbus_map
        self.host = host
        self.port = port
        self.timeout = timeout

        self.context = self._get_modbus_context()
        self.thread = threading.Thread(target=self.start_blocking, daemon=True)

        self._validator = ModbusMapValidator(self.modbus_map)
        self._register_type_to_function_code = {
            "co": 1,
            "di": 2,
            "hr": 3,
            "ir": 4,
        }

    def _get_modbus_context(self):

        context = {}
        for slave_id, slave in self.modbus_map.items():
            mb_slave_context = {}
            for mb_register_type, mb_register in slave.items():
                values = {mb_variable["address"]: 0 for mb_variable in mb_register.values()}
                mb_slave_context[mb_register_type] = ModbusSparseDataBlock(values)
            context[slave_id] = ModbusSlaveContext(**mb_slave_context, zero_mode=True)

        return ModbusServerContext(slaves=context, single=self._single)

    def start_blocking(self):

        asyncio.run(self._start_async())

    def start_non_blocking(self):

        self.thread.start()

    async def _start_async(self):

        self.server = _ModbusTcpServer(self.context, address=(self.host, self.port))
        await self.server.serve_forever()

    def stop(self, timeout: float = 5):

        asyncio.run_coroutine_threadsafe(self.server.shutdown(), self.server.loop)
        self.thread.join(timeout=timeout)

    def get_mb_value_from_address(self, register_type: str, address: int, slave_id: int = 0):

        f_code = self._register_type_to_function_code[register_type]
        return self.context[slave_id].getValues(f_code, address, count=1)[0]

    def get_mb_value(
            self,
            mb_variable_name: str,
            register_type: str,
            slave_id: int = 0,
            address: int = None,
    ):

        if address is None:

            self._validator.check_mb_variable_name(slave_id, register_type, mb_variable_name)
            mb_variable = self.modbus_map[slave_id][register_type][mb_variable_name]
            address = address or mb_variable["address"]

        f_code = self._register_type_to_function_code[register_type]
        mb_value = self.context[slave_id].getValues(f_code, address, count=1)[0]
        return mb_value

    def set_mb_value(
            self,
            mb_variable_name: str,
            register_type: str,
            value: int,
            slave_id: int = 0,
            address: int = None,
    ):

        if address is None:

            self._validator.check_mb_variable_name(slave_id, register_type, mb_variable_name)
            mb_variable = self.modbus_map[slave_id][register_type][mb_variable_name]
            address = address or mb_variable["address"]

        f_code = self._register_type_to_function_code[register_type]
        self.context[slave_id].setValues(f_code, address, [value])

import asyncio
import threading

from pymodbus.datastore import ModbusSlaveContext, ModbusSparseDataBlock, ModbusServerContext
from pymodbus.server import ModbusTcpServer as _ModbusTcpServer

from ._auxiliary_functions import is_type

ModbusMapTypeSingleSlave = dict[str, dict[str, str | int]]
ModbusMapTypeMultipleSlaves = dict[int, ModbusMapTypeSingleSlave]


class ModbusTcpServer:

    def __init__(
            self,
            modbus_map: ModbusMapTypeMultipleSlaves | ModbusMapTypeSingleSlave,
            host: str = "127.0.0.1",
            port: int = 502,
            timeout=0.5,
    ):

        if is_type(modbus_map, ModbusMapTypeSingleSlave):
            modbus_map = {0: modbus_map}
            self._single = True
        else:
            self._single = False

        self.modbus_map = modbus_map
        self.host = host
        self.port = port
        self.timeout = timeout

    def _get_modbus_context(self):

        context = {}
        for slave_id, slave in self.modbus_map.items():
            mb_slave_context = {}
            for mb_register_type, mb_register in slave.items():
                values = {mb_variable["address"]: 0 for mb_variable in mb_register.values()}
                mb_slave_context[mb_register_type] = ModbusSparseDataBlock(values)
            context[slave_id] = ModbusSlaveContext(**mb_slave_context)

        return ModbusServerContext(slaves=context, single=self._single)

    def start_blocking(self):

        asyncio.run(self._start_async())

    def start_non_blocking(self):

        th = threading.Thread(target=self.start_blocking, daemon=True)
        th.start()

    async def _start_async(self):

        context = self._get_modbus_context()

        self.server = _ModbusTcpServer(context, address=(self.host, self.port))
        await self.server.serve_forever()

    def get_mb_value(self, slave_id, register_type, address, count=1):

        return self.server.context[slave_id].getValues(4, address, count)

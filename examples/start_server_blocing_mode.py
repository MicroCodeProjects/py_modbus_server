import yaml
from py_modbus_server.modbus_tcp_server import ModbusTcpServer

with open('examples/modbus_maps/modbus_map.yaml', 'r') as file:
    modbus_map = yaml.safe_load(file)

print(modbus_map)
server = ModbusTcpServer(modbus_map, '127.0.0.1', 502)
server.start_blocking()

# Read YAML content from a file
import time

import yaml

from py_modbus_server.modbus_tcp_server import ModbusTcpServer

with open('examples/modbus_maps/modbus_map.yaml', 'r') as file:
    modbus_map = yaml.safe_load(file)

# Print the parsed data
print(modbus_map)
server = ModbusTcpServer(modbus_map, '127.0.0.1', 502)
# server.server.serve_forever()
# server.start_blocking()
server.start_non_blocking()
print(server.get_mb_value_from_address("hr", 100, 0))
time.sleep(5)
print("Server stopped")
server.stop()

import time

from py_modbus_server import ModbusTcpServer
from unittest import TestCase


class TestModbusTcpServer(TestCase):

    def test_start_stop(self):

        server = ModbusTcpServer({})
        server.start_non_blocking()
        time.sleep(3)
        server.stop(timeout=5)
        assert not server.thread.is_alive()

from unittest import TestCase

import responses
from qbo import Qbo


class TestQbo(TestCase):
    def setUp(self):
        self.qbo = Qbo("https://test.test/")

    @responses.activate
    def test_name(self):
        response_json = {
            "name": "TEST123"
        }

        responses.add(responses.GET, 'https://test.test/settings/name', json=response_json, status=200)

        name = self.qbo.name()

        assert name == "TEST123"

    @responses.activate
    def test_maintenance_status(self):
        response_json = {
            "maximumDescaleValue": 40000,
            "currentDescaleValue": 10000,
            "machineDescaleStatus": 0,
            "maximumCleanValue": 80,
            "currentCleanValue": 40,
            "machineCleanStatus": 1,
            "rinsingStatus": 3
        }

        responses.add(responses.GET, 'https://test.test/status/maintenance', json=response_json, status=200)

        maintenance_status = self.qbo.maintenance_status()

        assert maintenance_status.maximum_descale_value == 40000
        assert maintenance_status.current_descale_value == 10000
        assert maintenance_status.descale_percent == 0.25
        assert maintenance_status.machine_descale_status == 0

        assert maintenance_status.maximum_clean_value == 80
        assert maintenance_status.current_clean_value == 40
        assert maintenance_status.clean_percent == 0.5
        assert maintenance_status.machine_clean_status == 1
        assert maintenance_status.rinsing_status == 3


    @responses.activate
    def test_machine_info(self):
        response_json = {
            "serialNumber": "111111",
            "macAddress": "AA:BB:CC:DD:EE:FF",
            "version": "V01.20.A123"
        }

        responses.add(responses.GET, 'https://test.test/machineInfo', json=response_json, status=200)

        machine_info = self.qbo.machine_info()

        assert machine_info.serial_number == "111111"
        assert machine_info.mac_address == "AA:BB:CC:DD:EE:FF"
        assert machine_info.version == "V01.20.A123"

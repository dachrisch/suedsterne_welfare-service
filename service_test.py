# coding=utf-8
from unittest import TestCase

import jsonpickle

from service import remote_app
from welfare import WelfareStatus


class DummySheetConnector:
    def __init__(self, dummy_range):
        self.__range = dummy_range

    def values_for_range(self, sheet_range):
        return self.__range


class TestWelfareApi(TestCase):
    def setUp(self):
        # creates a test client
        self.app = remote_app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_get_welfare_status(self):
        self.assertEqual(200, self.app.get('/welfare/api/v1.0/status').status_code)

    def test_get_welfare_shout_out(self):
        self.assertEqual(200, self.app.get('/welfare/api/v1.0/shout_out').status_code)

    def test_status_as_json(self):
        import service
        service.welfare_status = WelfareStatus(DummySheetConnector((('A', 'OK', 1, 2),)))
        response = self.app.get('/welfare/api/v1.0/status').data
        status = jsonpickle.decode(response)
        self.assertEqual(1, len(status))
        self.assertEqual('A', status[0]['name'])
        self.assertEqual('OK (1, 2)', status[0]['status'])

    def test_shout_out_as_json(self):
        import service
        service.welfare_status = WelfareStatus(DummySheetConnector((('A', 'OK', 1, 2),)))
        response = self.app.get('/welfare/api/v1.0/shout_out').data
        shout_out = jsonpickle.decode(response)
        self.assertEqual('unicorn dance', shout_out)

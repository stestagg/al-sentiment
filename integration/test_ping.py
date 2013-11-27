import requests
import unittest

import integration


class PingTest(unittest.TestCase):

    def test_ping(self):
        self.assertEqual(
            requests.get(integration.Webserver.BASE_URL + "_ping").text,
            "PONG")

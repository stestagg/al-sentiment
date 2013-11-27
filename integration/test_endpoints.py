import requests
import unittest

import integration


class EndpointTests(unittest.TestCase):

    """Run some simple tests to check that the endpoints all work"""

    def get(self, path):
        response = requests.get(integration.Webserver.BASE_URL + path)
        self.assertEqual(response.status_code, 200)
        return response

    def test_index(self):
        self.assertIn("Loading", self.get("").text)

    def test_update(self):
        self.assertEqual(
            self.get("update").json(),
            {
                "message": "No JSON object could be decoded",
                "success": False
            })

    def test_tweets(self):
        self.get("tweets")
        # TODO: load some tweets through the feed and try again

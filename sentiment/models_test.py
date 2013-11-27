import contextlib
import unittest

import sentiment.feed
import sentiment.models
import sentiment.testutil


class TweetTest(unittest.TestCase):

    def test_keyword_detection(self):
        for candidate in ["coke",
                          "COKE",
                          "coca-cola",
                          "diet cola",
                          "I LOVE CoKe"]:
            tweet = sentiment.models.Tweet(message=candidate)
            self.assertTrue(tweet.contains_keyword)
        for candidate in ["cake", "cola", "coccola"]:
            tweet = sentiment.models.Tweet(message=candidate)
            self.assertFalse(tweet.contains_keyword)

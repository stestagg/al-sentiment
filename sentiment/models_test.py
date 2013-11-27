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
                          "some coke please",
                          "I LOVE CoKe"]:
            tweet = sentiment.models.Tweet(message=candidate)
            self.assertTrue(tweet.contains_keyword)
        for candidate in ["cake", "cokea", "diet", "in diet need",
                          "cola", "coccola"]:
            tweet = sentiment.models.Tweet(message=candidate)
            self.assertFalse(tweet.contains_keyword)

    def test_sentiment_text(self):
        for value, sentiment_text in {
                0.0: "neutral",
                0.1: "positive",
                -0.1: "negative",
                1: "positive"
                }.iteritems():
            tweet = sentiment.models.Tweet(sentiment=value)
            self.assertEqual(tweet.sentiment_text, sentiment_text)

import contextlib
import unittest

import fin.patch

import sentiment.feed
import sentiment.models
import sentiment.testutil


class FeedTest(unittest.TestCase):

    def basic_tweet(self):
        return {
            "id": 1,
            "user_handle": "@one",
            "followers": 2,
            "message": "Test",
            "sentiment": 0.1,
        }

    def test_with_no_new_tweets(self):
        sentiment.feed.handle_new_tweets([])

    def test_adding_simple_tweet(self):
        with sentiment.testutil.temp_db():
            sentiment.feed.handle_new_tweets([self.basic_tweet()])
            users = list(sentiment.models.User.select())
            self.assertEqual(len(users), 1)
            self.assertEqual(users[0].handle, "@one")
            self.assertEqual(users[0].followers, 2)

            tweets = list(sentiment.models.Tweet.select())
            self.assertEqual(len(tweets), 1)
            self.assertEqual(tweets[0].message, "Test")
            self.assertEqual(tweets[0].sentiment, 0.1)
            self.assertEqual(tweets[0].message_id, 1)
            self.assertEqual(tweets[0].seen_count, 1)
            self.assertEqual(tweets[0].contains_keyword, False)

    def test_adding_duplicate(self):
        with sentiment.testutil.temp_db():
            sentiment.feed.handle_new_tweets(
                [self.basic_tweet(), self.basic_tweet()])
            # Should only be one user
            self.assertEqual(sentiment.models.User.select().count(), 1)
            # Should also only be one user
            tweets = list(sentiment.models.Tweet.select())
            self.assertEqual(len(tweets), 1)
            # but seen count is now two
            self.assertEqual(tweets[0].seen_count, 2)

    def test_feed_failures(self):
        # Here's to hoping that 404.example.com never exists
        with fin.patch.patch(sentiment.feed, "FEED_URL", "http://404.example.com"):
            self.assertIn(
                "nodename nor servname provided, or not known",
                sentiment.feed.fetch_tweets())

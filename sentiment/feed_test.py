import contextlib
import unittest

import sentiment.feed
import sentiment.models
import sentiment.testutil


class FeedTest(unittest.TestCase):

    def test_with_no_new_tweets(self):
        sentiment.feed.handle_new_tweets([])

    def test_adding_simple_tweet(self):
        with sentiment.testutil.temp_db():
            sentiment.feed.handle_new_tweets([
                {
                    "id": 1,
                    "user_handle": "@one",
                    "followers": 2,
                    "message": "Test",
                    "sentiment": 0.1,
                }])
            users = list(sentiment.models.User.select())
            self.assertEqual(len(users), 1)
            self.assertEqual(users[0].handle, "@one")
            self.assertEqual(users[0].followers, 2)

            tweets = list(sentiment.models.Tweet.select())
            self.assertEqual(len(tweets), 1)
            self.assertEqual(tweets[0].message, "Test")
            self.assertEqual(tweets[0].sentiment, 0.1)
            self.assertEqual(tweets[0].message_id, 1)

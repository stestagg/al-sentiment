import contextlib
import unittest

import sentiment.feed
import sentiment.models


@contextlib.contextmanager
def temp_db():
    sentiment.models.setup(":memory:")
    try:
        yield
    finally:
        for table in sentiment.models.DB.get_tables():
            # This is ugly!
            sentiment.models.DB.execute_sql('drop table "%s"' % table)


class FeedTest(unittest.TestCase):

    def test_with_no_new_tweets(self):
        sentiment.feed.handle_new_tweets([])

    def test_adding_simple_tweet(self):
        with temp_db():
            sentiment.feed.handle_new_tweets([
                {
                    "user_handle": "@one",
                    "followers": 2
                }])
            users = list(sentiment.models.User.select())
            self.assertEqual(len(users), 1)
            self.assertEqual(users[0].handle, "@one")
            self.assertEqual(users[0].followers, 2)

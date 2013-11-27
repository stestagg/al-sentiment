import requests

import sentiment.models


FEED_URL = "http://adaptive-test-api.herokuapp.com/tweets.json"


def fetch_tweets(feed_url=None):
    """Get the new tweets and ingest them.  Returns a string error message
    if anything goes wrong"""
    new_tweets = requests.get(FEED_URL).json()
    if isinstance(new_tweets, dict):
        return new_tweets.get("error", {}).get("message", "Unknown error")
    try:
        handle_new_tweets(new_tweets)
    except Exception, e:
        # TODO: don't return unguarded exception messages to user
        return e.message


def handle_new_tweets(tweets):
    for data in tweets:
        # Example: {"created_at":"2012-09-27T16:16:26Z","followers":9,"id":10,
        #            "message":"Coca cola sucks, man","sentiment":-0.6,
        #            "updated_at":"2012-09-27T16:16:26Z",
        #            "user_handle":"@disser_ono"}
        user = sentiment.models.User.get_and_update_followers(
            handle=data["user_handle"], followers=data["followers"])

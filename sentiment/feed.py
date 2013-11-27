import requests

import sentiment.models


FEED_URL = "http://adaptive-test-api.herokuapp.com/tweets.json"


def fetch_tweets():
    """Get the new tweets and ingest them.  Returns a string error message
    if anything goes wrong"""
    try:
        new_tweets = requests.get(FEED_URL).json()
        if isinstance(new_tweets, dict):
            return new_tweets.get("error", {}).get("message", "Unknown error")
        handle_new_tweets(new_tweets)
    except Exception as e:
        # TODO: don't return unguarded exception messages to user
        return str(e.message)


def handle_new_tweets(tweets):
    Tweet = sentiment.models.Tweet
    for data in tweets:
        # Example: {"created_at":"2012-09-27T16:16:26Z","followers":9,"id":10,
        #            "message":"Coca cola sucks, man",
        #            "sentiment":-0.6,
        #            "updated_at":"2012-09-27T16:16:26Z",
        #            "user_handle":"@disser_ono"}
        user = sentiment.models.User.get_and_update_followers(
            handle=data["user_handle"], followers=data["followers"])
        message_id = data["id"]
        existing = Tweet.select().where(Tweet.message_id == message_id).count()
        if existing:
            # This assumes that no two tweets will share the same ID
            # It also assumes that message duplication is based on the ID too
            Tweet.update(seen_count=Tweet.seen_count + 1).where(
                Tweet.message_id == message_id).execute()
        else:
            tweet = Tweet.create(
                message=data["message"],
                message_id=message_id,
                sentiment=data["sentiment"],
                user=user)

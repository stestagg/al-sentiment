import fin.module


# Find and import all database subclasses (from dbs/*.py)
fin.module.import_child_modules(["sentiment", "dbs"])


class Database(object):
    """
    An abstract database interface, modules in dbs/ implement this interface to
    access the data.

    This approach does not allow an ORM to be used easily, but does allow for
    easy DB abstraction which for a simple data store improves testability.
    """

    NAME = NotImplemented  # Subclasses should provide a terse, human-readable
                           # name that will be used to refer to the engine.

    @classmethod
    def get_database(cls, name):
        for subclass in self.__subclasses__:
            print subclass

    def add_tweet(self, id, score, timestamp, user, followers):
        """Record that a tweet has been seen"""
        raise NotImplementedError("add_tweet")

    def get_tweet_by_message(self, message):
        """Return a tweet with the matching message,
           or None if one doesn't exist
        """
        raise NotImplementedError("get_tweet_by_message")

    def get_tweets(self, limit=None, offset=0):
        """Get all tweets up to a certain limit,
           returns a list of Tweet objects
        """
        raise NotImplementedError("get_tweets")

    def get_tweet_by_user(self, user):
        """Given a user name, return all tweets for that user"""
        raise NotImplementedError("get_tweet_by_user")

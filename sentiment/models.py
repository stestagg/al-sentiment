import peewee
import re

# Create PeeWee DB model without initialising it
# The server is responsible for deciding the connection
# parameters
DB = peewee.SqliteDatabase(None, threadlocals=True)


def setup(connection_string):
    DB.init(connection_string)
    # Create any missing tables, this does not handle schema migrations (yet)
    for model in [User, Tweet]:
        if not model.table_exists():
            model.create_table()


class User(peewee.Model):

    class Meta:
        database = DB

    handle = peewee.TextField(primary_key=True)
    followers = peewee.IntegerField()

    @classmethod
    def get_and_update_followers(cls, handle, followers):
        try:
            user = User.get(handle=handle)
        except peewee.DoesNotExist:
            new = User.create(handle=handle, followers=followers)
            return new
        else:
            if user.followers != followers:
                user.followers = followers
                user.save()
            return user


class Tweet(peewee.Model):

    KEYWORD_MATCHER = re.compile(r"\b(coke|coca\-cola|diet cola)\b", re.I)

    class Meta:
        database = DB

    message_id = peewee.IntegerField(primary_key=True)
    user = peewee.ForeignKeyField(User, related_name="tweets")
    message = peewee.TextField()
    sentiment = peewee.FloatField(indexed=True)
    seen_count = peewee.IntegerField(default=1)

    @classmethod
    def by_sentiment(cls):
        """Get all tweets ordered by their sentiment value"""
        # TODO: pagination?
        return cls.select().order_by(Tweet.sentiment.desc())

    @property
    def contains_keyword(self):
        return self.KEYWORD_MATCHER.search(self.message) is not None

    @property
    def sentiment_text(self):
        if self.sentiment > 0:
            return "positive"
        if self.sentiment == 0:
            return "neutral"
        return "negative"

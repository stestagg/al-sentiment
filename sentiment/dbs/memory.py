
import sentiment.db


class MemoryDatabase(sentiment.db.Database):

    NAME = "memory"

    def __init__(self):
        self.tweets = []

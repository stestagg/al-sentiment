import peewee

# Create PeeWee DB model without initialising it
# The server is responsible for deciding the connection
# parameters
DB = peewee.SqliteDatabase(None)


def setup(connection_string):
    DB.init(connection_string)
    # Create any missing tables, this does not handle schema migrations (yet)
    for model in [User, Tweet]:
        if not model.table_exists():
            mode.create_table()


class User(peewee.Model):

    class Meta:
        database = DB

    handle = peewee.TextField(primary_key=True)
    followers = peewee.IntegerField()


class Tweet(peewee.Model):

    class Meta:
        database = DB

    message_id = peewee.IntegerField(primary_key=True)
    user = peewee.ForeignKeyField(User, related_name="tweets")
    message = peewee.TextField()
    updated_date = peewee.DateTimeField()
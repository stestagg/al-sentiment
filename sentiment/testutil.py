import contextlib

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

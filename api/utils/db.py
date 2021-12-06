import sqlite3
from contextlib import contextmanager


@contextmanager
def db_cursor(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    yield cursor

    conn.commit()
    conn.close()

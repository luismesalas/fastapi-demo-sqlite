import sqlite3
from contextlib import contextmanager

DB_FILE = "data/public_schools.db"


@contextmanager
def db_cursor(db_file, commit=True):
    # Init
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Enter
    yield cursor

    # Exit
    if commit:
        conn.commit()
    conn.close()


def query_db_all(db_file, table):
    with db_cursor(db_file, commit=False) as cursor:
        return cursor.execute(f"SELECT * FROM {table}").fetchall()


def query_db(db_file, table, fields):
    if not fields:
        return query_db_all(db_file, table)

    named_fields = [f"{field_name} = :{field_name}" for field_name in fields.keys()]
    named_fields_clause = ' AND '.join(named_fields)

    with db_cursor(db_file, commit=False) as cursor:
        return cursor.execute(f"SELECT * FROM {table} where {named_fields_clause}", fields).fetchall()


def insert_db(db_file, table, fields):
    insert_fields_clause = ", ".join(fields.keys())
    named_fields_clause = f":{', :'.join(fields.keys())}"

    try:
        with db_cursor(db_file, commit=True) as cursor:
            cursor.execute(f"INSERT INTO {table} ({insert_fields_clause}) values ({named_fields_clause})", fields)
    except sqlite3.IntegrityError:
        return False
    return True

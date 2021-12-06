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


def query_inner_join(db_file, table_left, table_right, field_key_left, field_key_right, field_filters_left,
                     field_filters_right):
    field_filters_left = {f"t1.{key}": val for key, val in field_filters_left.items()}
    field_filters_right = {f"t2.{key}": val for key, val in field_filters_right.items()}
    fields_with_table_prefix = {**field_filters_left, **field_filters_right}
    named_fields = [f"{field_name} = :{field_name.replace('.', '')}" for field_name in fields_with_table_prefix.keys()]
    named_fields_clause = ' AND '.join(named_fields)
    field_filters = {key.replace('.', ''): val for key, val in fields_with_table_prefix.items()}

    with db_cursor(db_file, commit=False) as cursor:
        return cursor.execute(
            f"SELECT * FROM {table_left} t1 INNER JOIN {table_right} t2 on t1.{field_key_left} = t2.{field_key_right} "
            f"where {named_fields_clause}", field_filters).fetchall()


def insert_db(db_file, table, fields):
    insert_fields_clause = ", ".join(fields.keys())
    named_fields_clause = f":{', :'.join(fields.keys())}"

    try:
        with db_cursor(db_file, commit=True) as cursor:
            num_inserted = cursor.execute(f"INSERT INTO {table} ({insert_fields_clause}) "
                                          f"values ({named_fields_clause})", fields).rowcount
            return num_inserted > 0
    except sqlite3.IntegrityError:
        return False


def update_db(db_file, table, field_id_name, field_id_value, fields_to_update):
    set_fields_clause = ", ".join([f"{field_name}= :{field_name}" for field_name in fields_to_update.keys()])
    fields_to_update[field_id_name] = field_id_value

    with db_cursor(db_file, commit=True) as cursor:
        num_updated = cursor.execute(f"UPDATE {table} SET {set_fields_clause} "
                                     f"WHERE {field_id_name}= :{field_id_name}", fields_to_update).rowcount
        return num_updated > 0


def delete_db(db_file, table, field_name, field_value):
    with db_cursor(db_file, commit=True) as cursor:
        num_deleted = cursor.execute(f"DELETE FROM {table} where {field_name}={field_value}").rowcount
        return num_deleted > 0

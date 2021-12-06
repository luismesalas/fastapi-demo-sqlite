import csv
import logging
import os

from api.utils.db import db_cursor, DB_FILE

logging_format = '[%(asctime)s][%(levelname)s] %(message)s'
logging.basicConfig(format=logging_format, level=logging.DEBUG)
logging.getLogger().setLevel(level=logging.DEBUG)

CSV_FILE = "data/plantilla-organica-centros-publicos.csv"


def delete_existing_db():
    if os.path.exists(DB_FILE):
        logging.info(f"Removing existing db in {DB_FILE}...")
        os.remove(DB_FILE)
        logging.info("Done.")


def init_empty_db():
    logging.info(f"Creating new db in {DB_FILE}...")
    with db_cursor(DB_FILE) as cursor:
        logging.info("Creating tables schools, positions and assignments...")
        cursor.execute('CREATE TABLE schools (code integer UNIQUE, name text, province text, locality text)')
        cursor.execute('CREATE TABLE positions (code text UNIQUE, name text, corps text)')
        cursor.execute('CREATE TABLE assignments (school integer, position text, quantity integer, '
                       'UNIQUE(school, position))')
    logging.info("Done.")


def load_dataset_from_csv():
    logging.info(f"Loading data from CSV file in {CSV_FILE}...")
    with open(CSV_FILE, newline='', encoding='iso-8859-1') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        schools = {}
        positions = {}
        assignments = []

        for row in csv_reader:
            school_id, school_name = row['CENTRO'].split('-', 1)
            position_id, position_name = row['PUESTO'].split('-', 1)
            # We overwrite by school_id regarding it apears n-times. Province and locality are tied up to school
            schools[school_id] = (school_id, school_name, row['PROVINCIA'], row['LOCALIDAD'])
            # We overwrite by position_id regarding it apears n-times. Corps is tied up to position
            positions[position_id] = (position_id, position_name, row['CUERPO'])
            # Finally, we add all the relations between schools and positions, including the quantity of those positions
            assignments.append((school_id, position_id, row['PLANTILLA']))

    logging.info(f"Returned schools, positions and assignments as list of tuples.")
    return list(schools.values()), list(positions.values()), assignments


def load_data():
    schools, positions, assignments = load_dataset_from_csv()

    logging.info(f"Inserting recors into {DB_FILE}...")
    with db_cursor(DB_FILE) as cursor:
        cursor.executemany("INSERT INTO schools (code, name, province, locality) values (?, ?, ?, ?)", schools)
        cursor.executemany("INSERT INTO positions (code, name, corps) values (?, ?, ?)", positions)
        cursor.executemany("INSERT INTO assignments (school, position, quantity) values (?, ?, ?)", assignments)
    logging.info(f"Done.")


if __name__ == "__main__":
    delete_existing_db()
    init_empty_db()
    load_data()

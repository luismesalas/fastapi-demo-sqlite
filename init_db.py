import csv
import os
import sqlite3


def delete_existing_db():
    if os.path.exists('data/public_schools.db'):
        os.remove('data/public_schools.db')


def init_empty_db():
    conn = sqlite3.connect('data/public_schools.db')
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE schools (code integer, name text, province text, locality text)')
    cursor.execute('CREATE TABLE positions (code integer, name text)')
    cursor.execute('CREATE TABLE assignment (corps text, school integer, position integer, quantity integer)')

    conn.commit()
    conn.close()


def load_data():
    with open('data/plantilla-organica-centros-publicos.csv', newline='', encoding='iso-8859-1') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        schools = {}
        positions = {}
        assignements = []
        for row in csv_reader:
            schools[row['CENTRO']] = {row['CENTRO'],row['PROVINCIA'],row['LOCALIDAD']}
            positions[row['PUESTO']] = {row['PUESTO']}
            assignements.append(row)


if __name__ == "__main__":
    delete_existing_db()
    init_empty_db()

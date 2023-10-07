import sqlite3
import csv

# Create the SQLite3 database
conn = sqlite3.connect("heroes.db")
cursor = conn.cursor()

# Create the heroes table
cursor.execute('''
    CREATE TABLE heroes (
        id INTEGER PRIMARY KEY,
        name TEXT,
        alias TEXT,
        age INTEGER,
        gender TEXT
    )
''')

# Create the powers_basic table
cursor.execute('''
    CREATE TABLE powers_basic (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT
    )
''')

# Create the powers table
cursor.execute('''
    CREATE TABLE powers (
        id INTEGER PRIMARY KEY,
        hero_id INTEGER,
        basic_power_id INTEGER,
        FOREIGN KEY (hero_id) REFERENCES heroes(id),
        FOREIGN KEY (basic_power_id) REFERENCES powers_basic(id)
    )
''')

# Create the Heroes_powers table
cursor.execute('''
    CREATE TABLE Heroes_powers (
        id INTEGER PRIMARY KEY,
        hero_id INTEGER,
        power_id INTEGER,
        FOREIGN KEY (hero_id) REFERENCES heroes(id),
        FOREIGN KEY (power_id) REFERENCES powers(id)
    )
''')

# Import data from CSV files into the respective tables
def import_csv_data(table_name, csv_file):
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Get the header row to determine the number of columns

        # Create the INSERT INTO statement dynamically based on the number of columns
        placeholders = ', '.join(['?'] * len(header))
        insert_sql = f'INSERT INTO {table_name} VALUES ({placeholders})'

        for row in csv_reader:
            cursor.execute(insert_sql, row)

import_csv_data('heroes', 'heroes.csv')
import_csv_data('powers_basic', 'powers_basic.csv')
import_csv_data('powers', 'powers.csv')
import_csv_data('Heroes_powers', 'Heroes_powers.csv')

# Commit changes and close the database connection
conn.commit()
conn.close()

# code to combine database tables into one database

import sqlite3
from pathlib import Path

# Define the path to the data folder
source_folder = Path('Model/working_outputs_inputs')
output_folder = Path('Model')

# Set the output database filename
db_filename = output_folder / 'database.db'

# Create the database connection
conn = sqlite3.connect(db_filename)

# Create a cursor object
cur = conn.cursor()



# create tables in the database

# Drop the tables if they exist
cur.execute("DROP TABLE IF EXISTS heroes_powers")
cur.execute("DROP TABLE IF EXISTS heroes")
cur.execute("DROP TABLE IF EXISTS powers")

# create the heroes table in the database
    # with primary key constraint
cur.execute("""
            CREATE TABLE heroes (
            hero_id INTEGER NOT NULL
            , hero_name TEXT NOT NULL
            , gender TEXT
            , eye_color TEXT
            , species TEXT
            , hair_color TEXT
            , height REAL
            , weight REAL
            , publisher TEXT
            , skin_color TEXT
            , alignmnet TEXT
            , PRIMARY KEY (hero_id)
            );
            """)

# create the powers table in the database
    # with primary key constraint
cur.execute("""
            CREATE TABLE powers (
            power_id INTEGER NOT NULL
            , power_name TEXT
            , power_type TEXT
            , power_level INTEGER
            , PRIMARY KEY (power_id)
            );
            """)

# create the heroes_powers table in the database
    # with primary/foreign key constraints
cur.execute("""
            CREATE TABLE heroes_powers (
            hero_id INTEGER NOT NULL
            , power_id INTEGER NOT NULL
            , PRIMARY KEY (hero_id, power_id)
            , FOREIGN KEY (hero_id) REFERENCES heroes (hero_id)
            , FOREIGN KEY (power_id) REFERENCES powers (power_id)
            );
            """)

# commit the changes
conn.commit()



# insert the heroes data

# connect to the heroes.db database
conn_heroes = sqlite3.connect(source_folder / 'heroes.db')

# create a cursor object
cur_heroes = conn_heroes.cursor()

# select all rows from the heroes table
cur_heroes.execute("SELECT * FROM heroes")

# insert the rows into the heroes table in the database
for row in cur_heroes.fetchall():
    cur.execute("INSERT INTO heroes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)

# commit the changes
conn.commit()

# close the heroes cursor and connection
cur_heroes.close()
conn_heroes.close()



# insert the powers data

# connect to the powers.db database
conn_powers = sqlite3.connect(source_folder / 'powers.db')

# create a cursor object
cur_powers = conn_powers.cursor()

# select all rows from the powers table
cur_powers.execute("SELECT * FROM powers")

# insert the rows into the powers table in the database
for row in cur_powers.fetchall():
    cur.execute("INSERT INTO powers VALUES (?, ?, ?, ?)", row)

# commit the changes
conn.commit()

# close the powers cursor and connection
cur_powers.close()
conn_powers.close()


# insert the heroes_powers data

# connect to the heroes_powers.db database
conn_heroes_powers = sqlite3.connect(source_folder / 'heroes_powers.db')

# create a cursor object
cur_heroes_powers = conn_heroes_powers.cursor()

# select all rows from the heroes_powers table
cur_heroes_powers.execute("SELECT * FROM heroes_powers")

# insert the rows into the heroes_powers table in the database
for row in cur_heroes_powers.fetchall():
    cur.execute("INSERT INTO heroes_powers VALUES (?, ?)", row)

# commit the changes
conn.commit()

# close the heroes_powers cursor and connection
cur_heroes_powers.close()
conn_heroes_powers.close()



# close the output cursor and connection
cur.close()
conn.close()
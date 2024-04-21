import psycopg2
from pathlib import Path
from .database_config import DATABASES

# Define the path to the data folder
source_folder = Path('GA _assignment_2/working_outputs_inputs')

# Use DATABASES settings for PostgreSQL connection parameters
conn_params = DATABASES['default']

# Create a connection to PostgreSQL database
conn = psycopg2.connect(**conn_params)

# Create a cursor object
cur = conn.cursor()

# Drop the tables if they exist
cur.execute("DROP TABLE IF EXISTS heroes_powers")
cur.execute("DROP TABLE IF EXISTS heroes")
cur.execute("DROP TABLE IF EXISTS powers")

# Create the heroes table in the database
cur.execute("""
            CREATE TABLE heroes (
            hero_id SERIAL PRIMARY KEY,
            hero_name TEXT NOT NULL,
            gender TEXT,
            eye_color TEXT,
            species TEXT,
            hair_color TEXT,
            height REAL,
            weight REAL,
            publisher TEXT,
            skin_color TEXT,
            alignment TEXT
            );
            """)

# Create the powers table in the database
cur.execute("""
            CREATE TABLE powers (
            power_id SERIAL PRIMARY KEY,
            power_name TEXT,
            power_type TEXT,
            power_level INTEGER
            );
            """)

# Create the heroes_powers table in the database
cur.execute("""
            CREATE TABLE heroes_powers (
            hero_id INTEGER REFERENCES heroes(hero_id),
            power_id INTEGER REFERENCES powers(power_id),
            PRIMARY KEY (hero_id, power_id)
            );
            """)

# Commit the changes
conn.commit()

# Insert the heroes data

# Connect to the heroes database
conn_heroes = psycopg2.connect(**conn_params)

# Create a cursor object
cur_heroes = conn_heroes.cursor()

# Select all rows from the heroes table
cur_heroes.execute("SELECT * FROM heroes")

# Insert the rows into the heroes table in the database
cur.executemany("INSERT INTO heroes (hero_name, gender, eye_color, species, hair_color, height, weight, publisher, skin_color, alignment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", cur_heroes.fetchall())

# Commit the changes
conn.commit()

# Close the heroes cursor and connection
cur_heroes.close()
conn_heroes.close()

# Insert the powers data

# Connect to the powers database
conn_powers = psycopg2.connect(**conn_params)

# Create a cursor object
cur_powers = conn_powers.cursor()

# Select all rows from the powers table
cur_powers.execute("SELECT * FROM powers")

# Insert the rows into the powers table in the database
cur.executemany("INSERT INTO powers (power_name, power_type, power_level) VALUES (%s, %s, %s)", cur_powers.fetchall())

# Commit the changes
conn.commit()

# Close the powers cursor and connection
cur_powers.close()
conn_powers.close()

# Insert the heroes_powers data

# Connect to the heroes_powers database
conn_heroes_powers = psycopg2.connect(**conn_params)

# Create a cursor object
cur_heroes_powers = conn_heroes_powers.cursor()

# Select all rows from the heroes_powers table
cur_heroes_powers.execute("SELECT * FROM heroes_powers")

# Insert the rows into the heroes_powers table in the database
cur.executemany("INSERT INTO heroes_powers (hero_id, power_id) VALUES (%s, %s)", cur_heroes_powers.fetchall())

# Commit the changes
conn.commit()

# Close the heroes_powers cursor and connection
cur_heroes_powers.close()
conn_heroes_powers.close()

# Close the cursor and connection
cur.close()
conn.close()


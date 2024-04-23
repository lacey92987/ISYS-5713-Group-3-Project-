# """
# Contains configuration functions for the database.
# If this file is run directly, it will create the database schema and load the data.
# """

# import sqlite3
# from controller import *

# ###
# # Database Configuration Functions
# ###

# def create_database_schema():
#     """Function to create the database file and schema."""

#     try:
#         with sqlite3.connect(DATABASE_FILE) as conn:
            
#             cur = conn.cursor()

#             # Drop the tables if they exist
#             cur.execute("DROP TABLE IF EXISTS heroes_powers")
#             cur.execute("DROP TABLE IF EXISTS heroes")
#             cur.execute("DROP TABLE IF EXISTS powers")

#             # create the heroes table in the database
#             cur.execute("""
#                 CREATE TABLE heroes (
#                 hero_id INTEGER NOT NULL
#                 , hero_name TEXT NOT NULL
#                 , gender TEXT
#                 , eye_color TEXT
#                 , species TEXT
#                 , hair_color TEXT
#                 , height REAL
#                 , weight REAL
#                 , publisher TEXT
#                 , skin_color TEXT
#                 , alignment TEXT
#                 , PRIMARY KEY (hero_id)
#                 );
#                 """)

#             # create the powers table in the database
#             cur.execute("""
#                 CREATE TABLE powers (
#                 power_id INTEGER NOT NULL
#                 , power_name TEXT
#                 , power_type TEXT
#                 , power_level INTEGER
#                 , PRIMARY KEY (power_id)
#                 );
#                 """)

#             # create the heroes_powers table in the database
#             cur.execute("""
#                 CREATE TABLE heroes_powers (
#                 hero_id INTEGER NOT NULL
#                 , power_id INTEGER NOT NULL
#                 , PRIMARY KEY (hero_id, power_id)
#                 , FOREIGN KEY (hero_id) REFERENCES heroes (hero_id)
#                 , FOREIGN KEY (power_id) REFERENCES powers (power_id)
#                 );
#                 """)
            
#             # commit the changes
#             conn.commit()
    
#     # Raise any exceptions
#     except Exception as e:
#         print("Error creating database schema: {}".format(e))
#         raise e

# def load_data():
#     """Function to load data into the database."""

#     if not HEROES_FILENAME.is_file() or not POWERS_FILENAME.is_file() or not HEROES_POWERS_FILENAME.is_file():
#         raise Exception("One or more of the data files does not exist at the expected location.")
    
#     try:
#         with sqlite3.connect(DATABASE_FILE) as conn:

#             cur = conn.cursor()

#             # delete data from the tables if they exist
#             cur.execute("DELETE FROM heroes_powers")
#             cur.execute("DELETE FROM heroes")
#             cur.execute("DELETE FROM powers")

#             # load data into the heroes table
#             with open(HEROES_FILENAME, 'r') as file:
#                 # Skip the header row
#                 next(file)

#                 for line in file:
#                     # Split each line into values and insert into the table
#                     row = line.strip().split(',')
#                     cur.execute("INSERT INTO heroes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))
            
#             # load the data into the powers table
#             with open(POWERS_FILENAME, 'r') as file:
#                 # Skip the header row
#                 next(file)

#                 for line in file:
#                     # Split each line into values and insert into the table
#                     row = line.strip().split(',')
#                     cur.execute("INSERT INTO powers VALUES (?, ?, ?, ?)", (int(row[0]), row[1], row[2], int(row[3])))
            
#             # load the data into the heroes_powers table
#             with open(HEROES_POWERS_FILENAME, 'r') as file:
#                 # Skip the header row
#                 next(file)

#                 for line in file:
#                     # Split each line into values and insert into the table
#                     row = line.strip().split(',')
#                     cur.execute("INSERT INTO heroes_powers VALUES (?, ?)", (int(row[0]), int(row[1])))
    
#     # Raise any exceptions
#     except Exception as e:
#         print("Error loading data: {}".format(e))
#         raise e

# create_database_schema()
# load_data()

import psycopg2
from controller import *

def create_database_schema():
    """Function to create the database schema."""
    try:
        conn = psycopg2.connect(**DATABASE_PARAMS)
        cur = conn.cursor()

        # Drop tables if they exist
        cur.execute("DROP TABLE IF EXISTS heroes_powers CASCADE")
        cur.execute("DROP TABLE IF EXISTS heroes CASCADE")
        cur.execute("DROP TABLE IF EXISTS powers CASCADE")

        # Create the heroes table
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
            )
        """)

        # Create the powers table
        cur.execute("""
            CREATE TABLE powers (
                power_id SERIAL PRIMARY KEY,
                power_name TEXT,
                power_type TEXT,
                power_level INTEGER
            )
        """)

        # Create the heroes_powers table
        cur.execute("""
            CREATE TABLE heroes_powers (
                hero_id INTEGER REFERENCES heroes(hero_id),
                power_id INTEGER REFERENCES powers(power_id),
                PRIMARY KEY (hero_id, power_id)
            )
        """)

        conn.commit()
        cur.close()
        conn.close()
    
    except Exception as e:
        print("Error creating database schema: {}".format(e))
        raise e

def load_data():
    """Function to load data into the database."""
    if not HEROES_FILENAME.is_file() or not POWERS_FILENAME.is_file() or not HEROES_POWERS_FILENAME.is_file():
        raise Exception("One or more of the data files does not exist at the expected location.")

    try:
        conn = psycopg2.connect(**DATABASE_PARAMS)
        cur = conn.cursor()

        # Load data into the heroes table
        with open(HEROES_FILENAME, 'r') as file:
            next(file)  # Skip header
            cur.copy_from(file, 'heroes', sep=',')

        # Load data into the powers table
        with open(POWERS_FILENAME, 'r') as file:
            next(file)  # Skip header
            cur.copy_from(file, 'powers', sep=',')

        # Load data into the heroes_powers table
        with open(HEROES_POWERS_FILENAME, 'r') as file:
            next(file)  # Skip header
            cur.copy_from(file, 'heroes_powers', sep=',')

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print("Error loading data: {}".format(e))
        raise e

create_database_schema()
load_data()

"""
Contains paths to the database and data files.
"""

##from pathlib import Path

# Define the path to the 'data' folder
##DATA_FOLDER = Path('data')

# Set the output database filename
##DATABASE_FILE = DATA_FOLDER / 'database.db'

# Set the input data filenames
##HEROES_FILENAME = DATA_FOLDER / 'heroes.csv'
##POWERS_FILENAME = DATA_FOLDER / 'powers.csv'
##HEROES_POWERS_FILENAME = DATA_FOLDER / 'heroes_powers_convert.csv'

import os
import psycopg2

db_params = {
    'user': 'lcdouglas',
    'password': 'N3/tle12',
    'host': 'lcdouglas.postgres.database.azure.com',
    'port': 5432,
    'database': 'database'
}




# Define the table names
HEROES_TABLE = 'heroes'
POWERS_TABLE = 'powers'
HEROES_POWERS_TABLE = 'heroes_powers_convert'

# Python file to contain all the queries used in the project
    # Basic function run_query to connect to database & execute a query
    # Each query inside a named function that makes use of the run_query function

    # Currently, returns results as a pandas dataframe
    # Will need to be updated to return results as object(s) of a class (Hero, Power, etc.)


import sqlite3
import pandas as pd
from pathlib import Path


# Define the path to the database
db_file = Path.cwd() / 'database.db'


# Define basic function to return a database and return a dataframe
# Using the with keyword to ensure the connection is closed after query is executed
def run_query(db_file, query_text='', params=None):
    with sqlite3.connect(db_file) as cnn:
        return pd.read_sql(query_text, cnn, params=params)

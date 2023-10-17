# Python file to contain all the queries used in the project
    # Basic function run_query to connect to database & execute a query
    # Each query inside a named function that makes use of the run_query function

    # Currently, returns results as a pandas dataframe
    # Will need to be updated to return results as object(s) of a class (Hero, Power, etc.)



import sqlite3
import pandas as pd
from pathlib import Path


# Define the path to the database
db_file = 'Model\database.db'


# Define basic function to query the database and return a dataframe
def run_query(query_text, params=None):
    # 'with' keyword ensures the connection is closed after query is executed
    with sqlite3.connect(db_file) as cnn:
        return pd.read_sql(query_text, cnn, params=params)




# TEST INPUTS

query_text = """
    SELECT *
    FROM heroes_powers hp, powers p
    WHERE hp.power_id = p.power_id
        AND hp.hero_id = ?;
    """
params = (1,)

results = run_query(query_text, db_file, params)
print(results)



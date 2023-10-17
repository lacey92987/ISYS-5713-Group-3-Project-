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



# Function to get all powers for a given hero_id
def get_powers_for_hero_id(hero_id):
    query_text = """
        SELECT p.power_id, p.power_name, p.power_type, p.power_level
        FROM heroes_powers hp, powers p
        WHERE hp.power_id = p.power_id
            AND hp.hero_id = ?;
        """
    params = (hero_id,)

    results = run_query(query_text, params)

    return results


# TEST INPUTS

powers_result = get_powers_for_hero_id(2)
print(powers_result)

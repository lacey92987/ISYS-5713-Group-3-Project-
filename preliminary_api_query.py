# Preliminary file to test one query and API function in a single file

import sqlite3
import pandas as pd
from pathlib import Path

# define a class for powers
class Power:
    """Class for a power"""
    def __init__(self, power_name, power_level=0, power_type=None, power_id=None):
        self.power_id = power_id
        self.power_name = power_name
        self.power_type = power_type
        self.power_level = power_level

# specify the database file
data_folder = Path("Model")
db_file = data_folder / "database.db"


# basic function to run a query and return a dataframe, closing the connection when done
def run_query(query, db_file, params=None):
    with sqlite3.connect(db_file) as cnn:
        return pd.read_sql(query, cnn, params=params)
    

# define a query to get a power by id
def get_power(id):
    query = "SELECT * FROM powers WHERE power_id = ?;"
    params = (id,)
    results = run_query(query, db_file, params)
    return results

# test
id = 10
test_result= get_power(id)
print(test_result)
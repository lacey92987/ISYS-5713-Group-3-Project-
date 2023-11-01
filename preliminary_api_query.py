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


# Basic function to run a query, closing the connection using the with statement
def run_query(query, db_file, fetchone=False, params=()):
    """Executes a query and returns the results as tuple(s), closing the connection."""
    with sqlite3.connect(db_file) as cnn:
        cur = cnn.cursor()
        cur.execute(query, params)
        if fetchone:
            return cur.fetchone()
        else:
            return cur.fetchall()


# define a query to get a power by id
def get_power(id):
    query = "SELECT * FROM powers WHERE power_id = ?;"
    params = (id,)
    results = run_query(query, db_file, True, params)
    return results

# test
id = 10
test_result= get_power(id)
print(test_result)
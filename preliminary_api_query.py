# Preliminary file to test one query and API function in a single file

import sqlite3
import pandas as pd
from pathlib import Path

# basic function to run a query and return a dataframe, closing the connection when done
def run_query(query, db_file, params=None):
    with sqlite3.connect(db_file) as cnn:
        return pd.read_sql(query, cnn, params=params)
    



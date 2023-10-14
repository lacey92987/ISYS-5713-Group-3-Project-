# Python file to contain all the queries used in the project
    # Basic function run_query to connect to database & execute a query
    # Each query inside a named function that makes use of the run_query function

    # Currently, returns results as a pandas dataframe
    # Will need to be updated to return results as object(s) of a class (Hero, Power, etc.)

import sqlite3
import pandas as pd
from pathlib import Path
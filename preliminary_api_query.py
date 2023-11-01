# Preliminary file to test one query and API function in a single file

import sqlite3
from pathlib import Path
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

###
# Setup
###
app = Flask(__name__) 
CORS(app)
data_folder = Path("Model")
db_file = data_folder / "database.db"

###
# Routes
###
@app.route('/')
def index():
    return 'Hello, World!'


# define a class for powers
class Power:
    """Class for a power"""
    def __init__(self, power_name, power_level=0, power_type=None, power_id=None):
        self.power_name = power_name
        self.power_level = power_level
        self.power_type = power_type
        self.power_id = power_id
    
    def to_dictionary(self):
        """Returns a dictionary representation of the power"""
        power = {
            "power_name": self.power_name,
            "power_level": self.power_level,
            "power_type": self.power_type,
            "power_id": self.power_id
        }
        return power


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
    query = """
        SELECT power_name, power_level, power_type, power_id
        FROM powers
        WHERE power_id = ?;
        """
    params = (id,)
    result = run_query(query, db_file, True, params)
    if result is None:
        return None
    else:
        power = Power(result[0], result[1], result[2], result[3])
        return power

# test
id = 10
test_result= get_power(id)
dictionary = test_result.to_dictionary()
print(dictionary)
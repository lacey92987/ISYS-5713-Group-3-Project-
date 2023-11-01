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


@app.route('/v0/powers/<id>', methods=['GET'])
def get_power(id):
    """Returns a power by id, in JSON dictionary format"""
    power = select_power(id)
    if power is None:
        return jsonify(None), 404
    else:
        return jsonify(power.to_dictionary())


###
# Classes
###
class Power:
    """Class to represent a power."""
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

###
# Queries
###
def run_query(query, db_file, fetchone=False, params=()):
    """
    Executes a query and returns the results as tuple(s), closing the connection.
    
    Parameters
    ----------
    query : str
        The query to execute
    db_file : str
        The path to the database file
    fetchone : bool, optional
        If True, returns only the first result (as one tuple).
        If False, returns all results (as a list of tuples).
        Default is False.
    params : tuple, optional
        The parameters to pass to the query. Default is empty tuple.
    """

    with sqlite3.connect(db_file) as cnn:
        cur = cnn.cursor()
        cur.execute(query, params)
        if fetchone:
            return cur.fetchone()
        else:
            return cur.fetchall()


def select_power(id):
    """Returns a power by id, as a Power object"""
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


###
# Main
###
if __name__ == '__main__':
    # This says: if this file is run directly, then run the Flask app
    app.run(debug=False, use_reloader=False, passthrough_errors=True)
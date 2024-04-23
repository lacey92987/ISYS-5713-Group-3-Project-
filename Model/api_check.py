from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import sqlite3
from pathlib import Path

###

# Setup
###
app = Flask(__name__) 
CORS(app)
DB_PATH = Path.cwd() 
DATABASE_FILE = DB_PATH / 'database.db'

###
# Routes
# ###
# @app.route('/')
# def index():
#     return 'Hello, World!'


# @app.route('/heroes', methods=['GET'])
# def get_heroes():
#     all_heroes = select_all_heroes()
#     # Return the heroes as a JSON object
#     return jsonify(all_heroes)

# def select_all_heroes():
#     ''' Get all heroes from the database
#     '''
#     print(DATABASE_FILE)
#     conn = sqlite3.connect(DATABASE_FILE)
#     cur = conn.cursor()
#     # Get all heroes from the heroes table
#     cur.execute('SELECT * FROM heroes')
#     return cur.fetchall()

import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# PostgreSQL connection parameters
DATABASE_PARAMS = {
    'host': 'lcdouglas.postgres.database.azure.com',
    'port': '5432',
    'dbname': 'database',
    'user': 'lcdouglas',
    'password': 'N3/tle12'
}

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/heroes', methods=['GET'])
def get_heroes():
    all_heroes = select_all_heroes()
    return jsonify(all_heroes)

def select_all_heroes():
    try:
        # Establish connection to PostgreSQL database
        conn = psycopg2.connect(**DATABASE_PARAMS)
        cur = conn.cursor()
        
        # Execute query to get all heroes from the heroes table
        cur.execute('SELECT * FROM heroes')
        
        # Fetch all rows
        heroes = cur.fetchall()
        
        # Close cursor and connection
        cur.close()
        conn.close()
        
        return heroes
    except psycopg2.Error as e:
        print(f"Error retrieving heroes: {e}")
        return []

if __name__ == '__main__':
    app.run(debug=True)


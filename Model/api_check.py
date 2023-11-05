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
###
@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/heroes', methods=['GET'])
def get_heroes():
    all_heroes = select_all_heroes()
    # Return the heroes as a JSON object
    return jsonify(all_heroes)

def select_all_heroes():
    ''' Get all heroes from the database
    '''
    print(DATABASE_FILE)
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    # Get all heroes from the heroes table
    cur.execute('SELECT * FROM heroes')
    return cur.fetchall()

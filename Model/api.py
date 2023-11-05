from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import sqlite3
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

app = Flask(__name__) 
CORS(app)
DB_PATH = Path.cwd() / 'Model'
DATABASE_FILE = DB_PATH / 'database.db'


# Original database file used in reset_database()
ORIGINAL_DB_PATH = Path.cwd() / 'GA _assignment_2'
ORIGINAL_DATABASE_FILE = ORIGINAL_DB_PATH / 'database.db'



@app.route('/')
def index():
    return 'Hello, World!'

###
# Classes
###
@dataclass
class Power:
    """Class to represent a power."""
    power_name: str
    power_level: int = 0
    power_type: str = None
    power_id: int = None
    
    def to_dictionary(self):
        """Returns a dictionary representation of the power"""
        power = {
            "power_name": self.power_name,
            "power_level": self.power_level,
            "power_type": self.power_type,
            "power_id": self.power_id
        }
        return power

@dataclass
class Hero:
    """Class to represent a hero."""
    hero_name: str
    gender: str = None
    eye_color: str = None
    species: str = None
    hair_color: str = None
    height: float = None
    weight: float = None
    publisher: str = None
    skin_color: str = None
    alignment: str = None
    hero_id: int = None
    powers: List[Power] = field(default_factory=list)
    
    def to_dictionary(self):
        """Returns a dictionary representation of the hero"""
        hero = {
            "hero_name": self.hero_name,
            "gender": self.gender,
            "eye_color": self.eye_color,
            "species": self.species,
            "hair_color": self.hair_color,
            "height": self.height,
            "weight": self.weight,
            "publisher": self.publisher,
            "skin_color": self.skin_color,
            "alignment": self.alignment,
            "hero_id": self.hero_id,
            "powers": [power.to_dictionary() for power in self.powers]
        }
        return hero

    

###
# Routes and Queries
###

@app.route('/config/reset_database', methods=['PUT'])
def reset_database():
    """
    Resets the database to the original data by copying the original database file.
    The function will only execute if the whole process is successful, so the database will not be left in a broken state.
    Otherwise, an error will be returned and the database will not be changed.

    The original database file is specified in the ORIGINAL_DATABASE_FILE variable.

    Note, resets the contents but does not reset the schema. (I.e. the tables are not dropped and recreated.)
    Note, this does not check whether the database is already in the original state.
        (I.e. a success message does not necessarily mean there were any changes to reset.)
    """
    # If the ORIGINAL_DATABASE_FILE does not exist, return an error and stop the function
    if not ORIGINAL_DATABASE_FILE.is_file():
        return jsonify({"error": "The original database file does not exist at the expected path. The database has not been reset."}), 500
    
    # Uses the try keyword to ensure 
    try:
        # Clear the database
        conn = sqlite3.connect(DATABASE_FILE)
        cur = conn.cursor()
        cur.execute('DELETE FROM heroes_powers')
        cur.execute('DELETE FROM heroes')
        cur.execute('DELETE FROM powers')
        conn.commit()
        conn.close()

        # Copy the original database file
        conn = sqlite3.connect(ORIGINAL_DATABASE_FILE)
        cur = conn.cursor()
        cur.execute('SELECT * FROM heroes')
        heroes = cur.fetchall()
        cur.execute('SELECT * FROM powers')
        powers = cur.fetchall()
        cur.execute('SELECT * FROM heroes_powers')
        heroes_powers = cur.fetchall()
        conn.close()

        # Insert the original data into the database
        conn = sqlite3.connect(DATABASE_FILE)
        cur = conn.cursor()
        cur.executemany('INSERT INTO heroes VALUES (?,?,?,?,?,?,?,?,?,?,?)', heroes)
        cur.executemany('INSERT INTO powers VALUES (?,?,?,?)', powers)
        cur.executemany('INSERT INTO heroes_powers VALUES (?,?)', heroes_powers)
        conn.commit()
        conn.close()

        return jsonify({"message": "The database was successfully reset to the original state."}), 200

    except Exception as e:
        print("An error occurred while resetting the database. The database has not been reset.")
        print(e)
        return jsonify({"error": "An error occurred while resetting the database. The database has not been reset."}), 500

# GET - at least one for every table (except mapping tables)

# Get all (must have a filter) LIMIT

@app.route('/heroes', methods=['GET'])
def get_heroes():

    limit = request.args.get('limit', 10)

    heroes = select_all_heroes(limit)
    return jsonify([hero.to_dictionary() for hero in heroes])

def select_all_heroes(limit):
     
    print(DATABASE_FILE)
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    # Get column names from the sales table
    cur.execute('SELECT * FROM heroes LIMIT ?', (limit,))
    results = cur.fetchall()
    heroes = []
    for result in results:
        hero = Hero(result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10], result[0])
        heroes.append(hero)
    return heroes

@app.route('/powers', methods=['GET'])
def get_powers():
    
    limit = request.args.get('limit', 10)

    powers = select_all_powers(limit)
    return jsonify([power.to_dictionary() for power in powers])

def select_all_powers(limit):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cur = conn.cursor()
        cur.execute('SELECT * FROM powers LIMIT ?', (limit,))
        results = cur.fetchall()
        powers = []
        for result in results:
            power = Power(result[1], result[2], result[3], result[0])
            powers.append(power)
        return powers
    except Exception as e:
        print(f"Error in select_all_powers: {str(e)}")
        return None

# Get one by one
@app.route('/heroes/<id>', methods = ['GET'])
def get_hero(id):
    hero = select_hero(id)
    if hero is None:
        return jsonify({"error": "Hero not found"}), 404
    return jsonify(hero.to_dictionary()), 200

def select_hero(id):
    print(DATABASE_FILE)
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM heroes WHERE hero_id = ?', (id,))
    result = cur.fetchone()
    print(result)
    if result is None:
        return None
    hero = Hero(result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10], result[0])
    print(hero.to_dictionary())
    return hero

@app.route('/powers/<id>', methods = ['GET'])
def get_power(id):
    power = select_power(id)
    if power is None:
        return jsonify({"error": "Power not found"}), 404
    return jsonify(power.to_dictionary()), 200

def select_power(id):
    print(DATABASE_FILE)
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    # Get column names from the sales table
    cur.execute('SELECT * FROM powers WHERE power_id = ?', (id,))
    result = cur.fetchone()
    print(result)
    if result is None:
        return None
    power = Power(result[1], result[2], result[3], result[0])
    print(power.to_dictionary())
    return power

# Get that spans multiple tables (Heroes/powers/heroes_powers)


@app.route('/heroes/<id>/powers', methods = ['GET'])
def get_powers_by_hero(id):
    powers = select_powers_by_hero(id)
    return jsonify([power.to_dictionary() for power in powers])

def select_powers_by_hero(hero_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute('''
                SELECT p.power_name as "Name", p.power_level as "Level", p.power_type as "Type", p.power_id as "Id"
                FROM heroes AS h
                    JOIN heroes_powers AS hp ON h.hero_id = hp.hero_id
                    JOIN powers AS p ON hp.power_id = p.power_id
                WHERE h.hero_id = ?
                ''',
                (hero_id,))
    results = cur.fetchall()
    powers = []
    for result in results:
        power = Power(result[0], result[1], result[2], result[3])
        powers.append(power)
    return powers

# @app.get(/heroes{id}powers)
# def select_heroes_powers:

#     conn = sqlite3.connect(db_file)
#     cursor = conn.cursor()
#     cur.execute('''SELECT h.hero_name as "Name", p.power_name as "Power"
#     FROM heroes AS h
#     JOIN heroes_powers.heroes_powers AS hp ON h.hero_id = hp.hero_id
#     JOIN powers.powers AS p ON hp.power_id = p.power_id;
# ''')
#     return cur.fetchall()


# POST - Create a new entity for your database (can be a single table or multiple tables)
@app.route('/heroes', methods=['POST'])
def post_hero():
    pass

def insert_hero():

    hero_name = heroes.get('HeroName','')
    gender = heroes.get('Gender','')
    eye_color = heroes.get('EyeColor','')
    species = heroes.get('Species','')
    hair_color = heroes.get('HairColor','')
    height = heroes.get('Height','')
    weight = heroes.get('Weight','')
    publisher = heroes.get('Publisher','')
    skin_color = heroes.get('SkinColor','')
    alignment = heroes.get('Alignment','')
    
    if len(hero_name)==0:
        return jsonify({"error": "Missing required fields, 'HeroName'"}), 400

    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute('INSERT INTO heroes (HeroName, Gender, EyeColor, Species, HairColor, Height, Weight, Publisher, SkinColor, Alignment) VALUES (?,?,?,?,?,?,?,?,?,?)', 
                (hero_name, gender, eye_color, species, hair_color, height, weight, publisher, skin_color, alignment))
    conn.commit()
    print(cur.lastrowid)
    conn.close()
    return jsonify({"message": "Hero added successfully"}), 201

# PUT - Update an entity in your database
@app.route('/heroes',methods=['PUT'])
def put_hero():
    pass

def update_hero():

    hero_id = int(heroes.get('HeroId',-1))
    if hero_id < 0:
        return jsonify({"error": "Missing required fields, 'HeroId'"}), 400
    
    
    # This gets a little difficult, but we want to update the customer with the new data
    update_fields = []
    update_values = []
    
    if 'HeroName' in heores:
        hero_name = heroes.get('HeroName','')
        update_fields.append("HeroName=?")
        update_values.append(hero_name)
    
    if 'Gender' in heroes:
        gender = heroes.get('Gender','')
        update_fields.append("Gender=?")
        update_values.append(gender)
    
    if 'EyeColor' in heroes:
        eye_color = heroes.get('EyeColor','')
        update_fields.append("EyeColor=?")
        update_values.append(eye_color)
    
    if 'Species' in heores:
        species = heores.get('Species','')
        update_fields.append("Species=?")
        update_values.append(species)

    if 'HairColor' in heroes:
        hair_color = heroes.get('HairColor','')
        update_fields.append("HairColor=?")
        update_values.append(hair_color)
    
    if 'Height' in heroes:
        height = heroes.get('Height','')
        update_fields.append("Height=?")
        update_values.append(height)

    if 'Weight' in heroes:
        weight = heroes.get('Weight','')
        update_fields.append("Weight=?")
        update_values.append(weight)
    
    if 'Publisher' in heroes:
        publisher = heroes.get('Publisher','')
        update_fields.append("Publisher=?")
        update_values.append(publisher)
    
    if 'SkinColor' in heroes:
        skin_color = heroes.get('SkinColor','')
        update_fields.append("SkinColor=?")
        update_values.append(skin_color)
    
    if 'Alignment' in heroes:
        alignment = heroes.get('Alignment','')
        update_fields.append("Alignment=?")
        update_values.append(alignment)
    
    
    # Create the update statement
    update_statement = f'UPDATE heroes SET {",".join(update_fields)} WHERE HeroId = ?'
    update_values.append(hero_id)
    
    # Connect to the database and update the data   
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute(update_statement, update_values)
    conn.commit()
    
    # Now requery the database to get the updated fields
    cur.execute('SELECT * FROM heroes WHERE HeroId = ?', (hero_id,))
    return cur.fetchone()

# DELETE - Remove an entity from your database
@app.route('/heroes/<int:id>', methods=['DELETE'])
def delete_hero(id):
    pass

def remove_hero(id):
   
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute('DELETE FROM heroes WHERE HeroId = ?', (id,))
    conn.commit()
    return {'success':True}

###
# Main
###
if __name__ == '__main__':
    # This says: if this file is run directly, then run the Flask app
    app.run(debug=False, use_reloader=False, passthrough_errors=True)
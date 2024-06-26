# from flask import Flask
# from flask import jsonify
# from flask import request
# from flask_cors import CORS
# import sqlite3
# from pathlib import Path
# from dataclasses import dataclass, field, asdict
# from typing import List

# app = Flask(__name__) 
# CORS(app)
# DB_PATH = Path.cwd() / 'Model'
# DATABASE_FILE = DB_PATH / 'database.db'


# # Original database file used in reset_database()
# ORIGINAL_DB_PATH = Path.cwd() / 'GA _assignment_2'
# ORIGINAL_DATABASE_FILE = ORIGINAL_DB_PATH / 'database.db'



# @app.route('/')
# def index():
#     return 'Hello, World!'

# ###
# # Classes
# ###
# @dataclass
# class Power:
#     """Class to represent a power."""
#     power_name: str
#     power_level: int = 0
#     power_type: str = None
#     power_id: int = None
    
#     def to_dictionary(self):
#         """Returns a dictionary representation of the power"""
#         return asdict(self)

# @dataclass
# class Hero:
#     """Class to represent a hero."""
#     hero_name: str
#     gender: str = None
#     eye_color: str = None
#     species: str = None
#     hair_color: str = None
#     height: float = None
#     weight: float = None
#     publisher: str = None
#     skin_color: str = None
#     alignment: str = None
#     hero_id: int = None
#     powers: List[Power] = field(default_factory=list)
    
#     def to_dictionary(self, include_powers=False):
#         """Returns a dictionary representation of the hero"""
#         hero_dict = asdict(self)
#         if not include_powers:
#             hero_dict.pop('powers')
#         else:
#             hero_dict['powers'] = [power.to_dictionary() for power in self.powers]
#         return hero_dict

    

# ###
# # Routes and Queries
# ###

# @app.route('/config/reset_database', methods=['PUT'])
# def reset_database():
#     """
#     Resets the database to the original data by copying the original database file.
#     The function will only execute if the whole process is successful, so the database will not be left in a broken state.
#     Otherwise, an error will be returned and the database will not be changed.

#     The original database file is specified in the ORIGINAL_DATABASE_FILE variable.

#     Note, resets the contents but does not reset the schema. (I.e. the tables are not dropped and recreated.)
#     Note, this does not check whether the database is already in the original state.
#         (I.e. a success message does not necessarily mean there were any changes to reset.)
#     """
#     # If the ORIGINAL_DATABASE_FILE does not exist, return an error and stop the function
#     if not ORIGINAL_DATABASE_FILE.is_file():
#         return jsonify({"error": "The original database file does not exist at the expected path. The database has not been reset."}), 500
    
#     # Uses the try keyword to ensure 
#     try:
#         # Clear the database
#         conn = sqlite3.connect(DATABASE_FILE)
#         cur = conn.cursor()
#         cur.execute('DELETE FROM heroes_powers')
#         cur.execute('DELETE FROM heroes')
#         cur.execute('DELETE FROM powers')
#         conn.commit()
#         conn.close()

#         # Copy the original database file
#         conn = sqlite3.connect(ORIGINAL_DATABASE_FILE)
#         cur = conn.cursor()
#         cur.execute('SELECT * FROM heroes')
#         heroes = cur.fetchall()
#         cur.execute('SELECT * FROM powers')
#         powers = cur.fetchall()
#         cur.execute('SELECT * FROM heroes_powers')
#         heroes_powers = cur.fetchall()
#         conn.close()

#         # Insert the original data into the database
#         conn = sqlite3.connect(DATABASE_FILE)
#         cur = conn.cursor()
#         cur.executemany('INSERT INTO heroes VALUES (?,?,?,?,?,?,?,?,?,?,?)', heroes)
#         cur.executemany('INSERT INTO powers VALUES (?,?,?,?)', powers)
#         cur.executemany('INSERT INTO heroes_powers VALUES (?,?)', heroes_powers)
#         conn.commit()
#         conn.close()

#         return jsonify({"message": "The database was successfully reset to the original state."}), 200

#     except Exception as e:
#         print("An error occurred while resetting the database. The database has not been reset.")
#         print(e)
#         return jsonify({"error": "An error occurred while resetting the database. The database has not been reset."}), 500

# # GET - at least one for every table (except mapping tables)

# # Get all (must have a filter) LIMIT

# @app.route('/heroes', methods=['GET'])
# def get_heroes():

#     limit = request.args.get('limit', 10)

#     heroes = select_all_heroes(limit)
#     return jsonify([hero.to_dictionary() for hero in heroes])

# def select_all_heroes(limit):
     
#     print(DATABASE_FILE)
#     conn = sqlite3.connect(DATABASE_FILE)
#     cur = conn.cursor()
#     # Get column names from the sales table
#     cur.execute('SELECT * FROM heroes LIMIT ?', (limit,))
#     results = cur.fetchall()
#     heroes = []
#     for result in results:
#         hero = Hero(result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10], result[0])
#         heroes.append(hero)
#     return heroes

# @app.route('/powers', methods=['GET'])
# def get_powers():
    
#     limit = request.args.get('limit', 10)

#     powers = select_all_powers(limit)
#     return jsonify([power.to_dictionary() for power in powers])

# def select_all_powers(limit):
#     try:
#         conn = sqlite3.connect(DATABASE_FILE)
#         cur = conn.cursor()
#         cur.execute('SELECT * FROM powers LIMIT ?', (limit,))
#         results = cur.fetchall()
#         powers = []
#         for result in results:
#             power = Power(result[1], result[3], result[2], result[0])
#             powers.append(power)
#         return powers
#     except Exception as e:
#         print(f"Error in select_all_powers: {str(e)}")
#         return None

# # Get one by one
# @app.route('/heroes/<id>', methods = ['GET'])
# def get_hero(id):
#     hero = select_hero(id)
#     if hero is None:
#         return jsonify({"error": "Hero not found"}), 404
#     return jsonify(hero.to_dictionary()), 200

# def select_hero(id):
#     print(DATABASE_FILE)
#     conn = sqlite3.connect(DATABASE_FILE)
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM heroes WHERE hero_id = ?', (id,))
#     result = cur.fetchone()
#     print(result)
#     if result is None:
#         return None
#     hero = Hero(result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10], result[0])
#     print(hero.to_dictionary())
#     return hero

# @app.route('/powers/<id>', methods = ['GET'])
# def get_power(id):
#     power = select_power(id)
#     if power is None:
#         return jsonify({"error": "Power not found"}), 404
#     return jsonify(power.to_dictionary()), 200

# def select_power(id):
#     print(DATABASE_FILE)
#     conn = sqlite3.connect(DATABASE_FILE)
#     cur = conn.cursor()
#     # Get column names from the sales table
#     cur.execute('SELECT * FROM powers WHERE power_id = ?', (id,))
#     result = cur.fetchone()
#     print(result)
#     # Handle the case where the power with the given ID is not found
#     if result is None:
#         return None
#     power = Power(result[1], result[3], result[2], result[0])
#     print(power.to_dictionary())
#     return power

# # Get that spans multiple tables (Heroes/powers/heroes_powers)


# @app.route('/heroes/<id>/powers', methods=['GET'])
# def get_hero_powers(id):
#     hero_name, powers = select_hero_powers(id)
#     return jsonify({
#         "hero_name": hero_name,
#         "powers": [power.to_dictionary() for power in powers]
#     })

# def select_hero_powers(hero_id):
#     conn = sqlite3.connect(DATABASE_FILE)
#     cur = conn.cursor()
#     cur.execute('SELECT hero_name FROM heroes WHERE hero_id = ?', (hero_id,))
#     hero_result = cur.fetchone()

#     if hero_result:
#         hero_name = hero_result[0]
#     else:
#         return "Hero not found", []

#     cur.execute('''
#                 SELECT p.power_name, p.power_level, p.power_type, p.power_id
#                 FROM heroes AS h
#                 JOIN heroes_powers AS hp ON h.hero_id = hp.hero_id
#                 JOIN powers AS p ON hp.power_id = p.power_id
#                 WHERE h.hero_id = ?
#                 ''',
#                 (hero_id,))
#     power_results = cur.fetchall()
#     powers = []

#     for result in power_results:
#         power = Power(result[0], result[1], result[2], result[3])
#         powers.append(power)

#     return hero_name, powers


# # @app.get(/heroes{id}powers)
# # def select_heroes_powers:

# #     conn = sqlite3.connect(db_file)
# #     cursor = conn.cursor()
# #     cur.execute('''SELECT h.hero_name as "Name", p.power_name as "Power"
# #     FROM heroes AS h
# #     JOIN heroes_powers.heroes_powers AS hp ON h.hero_id = hp.hero_id
# #     JOIN powers.powers AS p ON hp.power_id = p.power_id;
# # ''')
# #     return cur.fetchall()


# # POST - Create a new entity for your database (can be a single table or multiple tables)
# @app.route('/heroes', methods=['POST'])
# def insert_hero():
#     data = request.get_json()

#     # Extract hero data from the JSON data
#     hero_name = data.get('hero_name', '')
#     gender = data.get('gender', '')
#     eye_color = data.get('eye_color', '')
#     species = data.get('species', '')
#     hair_color = data.get('hair_color', '')
#     height = data.get('height', 0.0)
#     weight = data.get('weight', 0.0)
#     publisher = data.get('publisher', '')
#     skin_color = data.get('skin_color', '')
#     alignment = data.get('alignment', '')

#     if len(hero_name) == 0:
#         return {"error": "Missing required field 'hero_name'"}, 400

#     conn = sqlite3.connect(DATABASE_FILE)
#     cur = conn.cursor()
#     cur.execute('INSERT INTO heroes (hero_name, gender, eye_color, species, hair_color, height, weight, publisher, skin_color,alignment) VALUES (?,?,?,?,?,?,?,?,?,?)',
#                 (hero_name, gender, eye_color, species, hair_color, height, weight, publisher, skin_color, alignment))
#     conn.commit()
#     hero_id = cur.lastrowid
#     conn.close()

#     response = {"message": "Hero added successfully", "hero_id": hero_id}
#     return response, 201




# # PUT - Update an entity in your database
# @app.route('/heroes/<int:hero_id>', methods=['PUT'])
# def update_hero(hero_id):
#     data = request.get_json()
#     response, status_code = modify_hero(hero_id, data)
#     return jsonify(response), status_code

# def modify_hero(hero_id, data):
#     # Extract hero data from the JSON data
#     hero_name = data.get('hero_name', '')
#     gender = data.get('gender', '')
#     eye_color = data.get('eye_color', '')
#     species = data.get('species', '')
#     hair_color = data.get('hair_color', '')
#     height = data.get('height', 0.0)
#     weight = data.get('weight', 0.0)
#     publisher = data.get('publisher', '')
#     skin_color = data.get('skin_color', '')
#     alignment = data.get('alignment', '')

#     conn = sqlite3.connect(DATABASE_FILE)
#     cur = conn.cursor()

#     update_fields = []
#     update_values = []

#     if 'hero_name' in data:
#         update_fields.append("hero_name=?")
#         update_values.append(hero_name)

#     if 'gender' in data:
#         update_fields.append("gender=?")
#         update_values.append(gender)

#     if 'eye_color' in data:
#         update_fields.append("eye_color=?")
#         update_values.append(eye_color)

#     if 'species' in data:
#         update_fields.append("species=?")
#         update_values.append(species)

#     if 'hair_color' in data:
#         update_fields.append("hair_color=?")
#         update_values.append(hair_color)

#     if 'height' in data:
#         update_fields.append("height=?")
#         update_values.append(height)

#     if 'weight' in data:
#         update_fields.append("weight=?")
#         update_values.append(weight)

#     if 'publisher' in data:
#         update_fields.append("publisher=?")
#         update_values.append(publisher)

#     if 'skin_color' in data:
#         update_fields.append("skin_color=?")
#         update_values.append(skin_color)

#     if 'alignment' in data:
#         update_fields.append("alignment=?")
#         update_values.append(alignment)

#     # Create the update statement
#     update_statement = f'UPDATE heroes SET {",".join(update_fields)} WHERE hero_id = ?'
#     update_values.append(hero_id)

#     cur.execute(update_statement, update_values)
#     conn.commit()

#     # Now requery the database to get the updated hero
#     updated_hero = select_hero(hero_id)

#     if updated_hero is not None:
#         return {"message": "Hero updated successfully", "hero": updated_hero.to_dictionary()}, 200
#     else:
#         return {"error": "Hero not found"}, 404




# # DELETE - Remove an entity from your database
# @app.route('/heroes/<int:id>', methods=['DELETE'])
# def delete_hero(id):
#     result = remove_hero(id)
#     if result['success']:
#         return jsonify({"message": "Hero deleted successfully"}), 200
#     else:
#         return jsonify({"error": "Hero not found"}), 404


# def remove_hero(id):
   
#     conn = sqlite3.connect(DATABASE_FILE)
#     cur = conn.cursor()
#     cur.execute('DELETE FROM heroes WHERE hero_id = ?', (id,))
#     conn.commit()
#     return {'success':True}

# #GET  function to compare two heroes power levels
# @app.route('/compare_power', methods=['GET'])
# def compare_power():
#     hero_id1 = request.args.get('hero_id1')
#     hero_id2 = request.args.get('hero_id2')

#     if not hero_id1 or not hero_id2:
#         return jsonify({"error": "Both hero_id1 and hero_id2 parameters are required"}), 400

#     conn = sqlite3.connect(DATABASE_FILE)
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT h1.hero_name AS hero_name1, SUM(p1.power_level) AS total_power1,
#            h2.hero_name AS hero_name2, SUM(p2.power_level) AS total_power2
#         FROM heroes AS h1
#         JOIN heroes_powers AS hp1 ON h1.hero_id = hp1.hero_id
#         JOIN powers AS p1 ON hp1.power_id = p1.power_id
#         JOIN heroes AS h2 ON h2.hero_id = ?
#         JOIN heroes_powers AS hp2 ON h2.hero_id = hp2.hero_id
#         JOIN powers AS p2 ON hp2.power_id = p2.power_id
#         WHERE h1.hero_id = ? AND h2.hero_id = ?
#     """, (hero_id2, hero_id1, hero_id2))

#     result = cursor.fetchone()
#     conn.close()

#     if result is None:
#         return jsonify({"error": "One or both heroes not found"}), 404

#     hero_name1, total_power1, hero_name2, total_power2 = result
#     if total_power1 > total_power2:
#         winner = hero_name1
#     elif total_power1 < total_power2:
#         winner = hero_name2
#     else:
#         winner = "Tie"

#     response = {
#         "hero_id1": hero_id1,
#         "hero_name1": hero_name1,
#         "total_power1": total_power1,
#         "hero_id2": hero_id2,
#         "hero_name2": hero_name2,
#         "total_power2": total_power2,
#         "winner": winner,
#     }

#     return jsonify(response)
    
# ###
# # Main
# ###
# if __name__ == '__main__':
#     # This says: if this file is run directly, then run the Flask app
#     app.run(debug=False, use_reloader=False, passthrough_errors=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import psycopg2
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List

app = Flask(__name__)
CORS(app)



db_params = {
    'user': 'lcdouglas',
    'password': 'N3/tle12',
    'host': 'lcdouglas.postgres.database.azure.com',
    'port': 5432,
    'database': 'database'
}

# Path to your database file
DB_PATH = Path.cwd() / 'Model'

# Original database file used in reset_database()
ORIGINAL_DB_PATH = Path.cwd() / 'GA_assignment_2'

@app.route('/')
def index():
    return 'Hello, World!'

# Classes
@dataclass
class Power:
    """Class to represent a power."""
    power_name: str
    power_level: int = 0
    power_type: str = None
    power_id: int = None
    
    def to_dictionary(self):
        """Returns a dictionary representation of the power"""
        return asdict(self)

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
    
    def to_dictionary(self, include_powers=False):
        """Returns a dictionary representation of the hero"""
        hero_dict = asdict(self)
        if not include_powers:
            hero_dict.pop('powers')
        else:
            hero_dict['powers'] = [power.to_dictionary() for power in self.powers]
        return hero_dict

# Routes and Queries

@app.route('/config/reset_database', methods=['PUT'])
def reset_database():
    try:
        # Clear the database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute('DELETE FROM heroes_powers')
        cur.execute('DELETE FROM heroes')
        cur.execute('DELETE FROM powers')
        conn.commit()

        # Copy the original database file
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM heroes')
                heroes = cur.fetchall()
                cur.execute('SELECT * FROM powers')
                powers = cur.fetchall()
                cur.execute('SELECT * FROM heroes_powers')
                heroes_powers = cur.fetchall()

        # Insert the original data into the database
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                cur.executemany('INSERT INTO heroes VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', heroes)
                cur.executemany('INSERT INTO powers VALUES (%s,%s,%s,%s)', powers)
                cur.executemany('INSERT INTO heroes_powers VALUES (%s,%s)', heroes_powers)
                conn.commit()

        return jsonify({"message": "The database was successfully reset to the original state."}), 200
    except psycopg2.Error as e:
        print("An error occurred while resetting the database. The database has not been reset.")
        print(e)
        return jsonify({"error": "An error occurred while resetting the database. The database has not been reset."}), 500

# GET - at least one for every table (except mapping tables)

@app.route('/heroes', methods=['GET'])
def get_heroes():
    limit = request.args.get('limit', 10)
    heroes = select_all_heroes(limit)
    return jsonify([hero.to_dictionary() for hero in heroes])

def select_all_heroes(limit):
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute('SELECT * FROM heroes LIMIT %s', (limit,))
        results = cur.fetchall()
        heroes = []
        for result in results:
            hero = Hero(result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10], result[0])
            heroes.append(hero)
        return heroes
    except psycopg2.Error as e:
        print(f"Error in select_all_heroes: {str(e)}")
        return []

@app.route('/powers', methods=['GET'])
def get_powers():
    limit = request.args.get('limit', 10)
    powers = select_all_powers(limit)
    return jsonify([power.to_dictionary() for power in powers])

def select_all_powers(limit):
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute('SELECT * FROM powers LIMIT %s', (limit,))
        results = cur.fetchall()
        powers = []
        for result in results:
            power = Power(result[1], result[3], result[2], result[0])
            powers.append(power)
        return powers
    except psycopg2.Error as e:
        print(f"Error in select_all_powers: {str(e)}")
        return None

# Get one by one

@app.route('/heroes/<id>', methods=['GET'])
def get_hero(id):
    hero = select_hero(id)
    if hero is None:
        return jsonify({"error": "Hero not found"}), 404
    return jsonify(hero.to_dictionary()), 200

def select_hero(id):
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute('SELECT * FROM heroes WHERE hero_id = %s', (id,))
        result = cur.fetchone()
        if result is None:
            return None
        hero = Hero(result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9], result[10], result[0])
        return hero
    except psycopg2.Error as e:
        print(f"Error in select_hero: {str(e)}")
        return None

@app.route('/powers/<id>', methods=['GET

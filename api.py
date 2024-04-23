# from flask import Flask
# from flask import jsonify
# from flask import request
# from flask_cors import CORS
# import sqlite3
# from pathlib import Path
# from dataclasses import dataclass, field, asdict
# from typing import List

# from controller import DATABASE_FILE
# from config import create_database_schema, load_data
# from model import *

# app = Flask(__name__) 
# CORS(app)


# ###
# # API Routes
# ###


# @app.route('/')
# def index():
#     return 'Hello, World!'


# @app.route('/config/reset_database', methods=['PUT'])
# def reset_database():
#     """
#     Resets the database to the original data using clean csv files.
#     The function will only execute if the whole process is successful, so the database will not be left in a broken state.
#     Otherwise, an error will be returned and the database will not be changed.

#     Note, by default, resets the contents but does not reset the schema. (I.e. the tables are not dropped and recreated.)
#     To recreate the schema, pass the reset_schema parameter as True.

#     Note, this does not check whether the database is already in the original state.
#         (I.e. a success message does not necessarily mean there were any changes to reset.)
#     """
    
#     reset_schema = request.args.get('reset_schema', False)

#     # Uses the try keyword to ensure the database is not left in a broken state
#     try:

#         # If the DATABASE_FILE does not exist or the reset_schema parameter is True, run the create_database_schema() function to [re]create it
#         if reset_schema == True or not DATABASE_FILE.is_file():
#             try:
#                 create_database_schema()
#             except Exception as e:
#                 print("An error occurred while resetting the database schema. The database has not been reset.")
#                 print(e)
#                 raise e

#         # Clear the database and insert the original data
#         try:
#             load_data()
#         except Exception as e:
#             print("An error occurred while resetting the database contents. The database has not been reset.")
#             print(e)
#             raise e
        
#         # If the database was successfully reset, return a success message
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


# @app.route('/powers', methods=['GET'])
# def get_powers():
    
#     limit = request.args.get('limit', 10)

#     powers = select_all_powers(limit)
#     return jsonify([power.to_dictionary() for power in powers])


# # Get one by one
# @app.route('/heroes/<id>', methods = ['GET'])
# def get_hero(id):
#     hero = select_hero(id)
#     if hero is None:
#         return jsonify({"error": "Hero not found"}), 404
#     return jsonify(hero.to_dictionary()), 200


# @app.route('/powers/<id>', methods = ['GET'])
# def get_power(id):
#     power = select_power(id)
#     if power is None:
#         return jsonify({"error": "Power not found"}), 404
#     return jsonify(power.to_dictionary()), 200



# # Get that spans multiple tables (Heroes/powers/heroes_powers)


# @app.route('/heroes/<id>/powers', methods=['GET'])
# def get_hero_powers(id):
#     hero_name, powers = select_hero_powers(id)
#     return jsonify({
#         "hero_name": hero_name,
#         "powers": [power.to_dictionary() for power in powers]
#     })


# # POST - Create a new entity for your database (can be a single table or multiple tables)
# @app.route('/heroes', methods=['POST'])
# def add_hero():
#     data = request.get_json()
#     response, status_code = insert_hero(data)
#     return jsonify(response), status_code


# # PUT - Update an entity in your database
# @app.route('/heroes/<int:hero_id>', methods=['PUT'])
# def update_hero(hero_id):
#     data = request.get_json()
#     response, status_code = modify_hero(hero_id, data)
#     return jsonify(response), status_code


# # DELETE - Remove an entity from your database
# @app.route('/heroes/<int:id>', methods=['DELETE'])
# def delete_hero(id):
#     result = remove_hero(id)
#     if result['success']:
#         return jsonify({"message": "Hero deleted successfully"}), 200
#     else:
#         return jsonify({"error": "Hero not found"}), 404


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


from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from pathlib import Path
from controller import DATABASE_PARAMS
from config import create_database_schema, load_data
from model import *

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/config/reset_database', methods=['PUT'])
def reset_database():
    reset_schema = request.args.get('reset_schema', False)

    try:
        if reset_schema == 'True' or not DATABASE_FILE.is_file():
            try:
                create_database_schema()
            except Exception as e:
                print("An error occurred while resetting the database schema. The database has not been reset.")
                print(e)
                raise e

        try:
            load_data()
        except Exception as e:
            print("An error occurred while resetting the database contents. The database has not been reset.")
            print(e)
            raise e

        return jsonify({"message": "The database was successfully reset to the original state."}), 200

    except Exception as e:
        print("An error occurred while resetting the database. The database has not been reset.")
        print(e)
        return jsonify({"error": "An error occurred while resetting the database. The database has not been reset."}), 500


@app.route('/heroes', methods=['GET'])
def get_heroes():
    limit = request.args.get('limit', 10)
    heroes = select_all_heroes(limit)
    return jsonify([hero.to_dictionary() for hero in heroes])


@app.route('/powers', methods=['GET'])
def get_powers():
    limit = request.args.get('limit', 10)
    powers = select_all_powers(limit)
    return jsonify([power.to_dictionary() for power in powers])


@app.route('/heroes/<id>', methods=['GET'])
def get_hero(id):
    hero = select_hero(id)
    if hero is None:
        return jsonify({"error": "Hero not found"}), 404
    return jsonify(hero.to_dictionary()), 200


@app.route('/powers/<id>', methods=['GET'])
def get_power(id):
    power = select_power(id)
    if power is None:
        return jsonify({"error": "Power not found"}), 404
    return jsonify(power.to_dictionary()), 200


@app.route('/heroes/<id>/powers', methods=['GET'])
def get_hero_powers(id):
    hero_name, powers = select_hero_powers(id)
    return jsonify({
        "hero_name": hero_name,
        "powers": [power.to_dictionary() for power in powers]
    })


@app.route('/heroes', methods=['POST'])
def add_hero():
    data = request.get_json()
    response, status_code = insert_hero(data)
    return jsonify(response), status_code


@app.route('/heroes/<int:hero_id>', methods=['PUT'])
def update_hero(hero_id):
    data = request.get_json()
    response, status_code = modify_hero(hero_id, data)
    return jsonify(response), status_code


@app.route('/heroes/<int:id>', methods=['DELETE'])
def delete_hero(id):
    result = remove_hero(id)
    if result['success']:
        return jsonify({"message": "Hero deleted successfully"}), 200
    else:
        return jsonify({"error": "Hero not found"}), 404


@app.route('/compare_power', methods=['GET'])
def compare_power():
    hero_id1 = request.args.get('hero_id1')
    hero_id2 = request.args.get('hero_id2')

    if not hero_id1 or not hero_id2:
        return jsonify({"error": "Both hero_id1 and hero_id2 parameters are required"}), 400

    conn = psycopg2.connect(**DATABASE_PARAMS)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT h1.hero_name AS hero_name1, SUM(p1.power_level) AS total_power1,
           h2.hero_name AS hero_name2, SUM(p2.power_level) AS total_power2
        FROM heroes AS h1
        JOIN heroes_powers AS hp1 ON h1.hero_id = hp1.hero_id
        JOIN powers AS p1 ON hp1.power_id = p1.power_id
        JOIN heroes AS h2 ON h2.hero_id = %s
        JOIN heroes_powers AS hp2 ON h2.hero_id = hp2.hero_id
        JOIN powers AS p2 ON hp2.power_id = p2.power_id
        WHERE h1.hero_id = %s AND h2.hero_id = %s
    """, (hero_id2, hero_id1, hero_id2))

    result = cursor.fetchone()
    conn.close()

    if result is None:
        return jsonify({"error": "One or both heroes not found"}), 404

    hero_name1, total_power1, hero_name2, total_power2 = result
    if total_power1 > total_power2:
        winner = hero_name1
    elif total_power1 < total_power2:
        winner = hero_name2
    else:
        winner = "Tie"

    response = {
        "hero_id1": hero_id1,
        "hero_name1": hero_name1,
        "total_power1": total_power1,
        "hero_id2": hero_id2,
        "hero_name2": hero_name2,
        "total_power2": total_power2,
        "winner": winner,
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, passthrough_errors=True)

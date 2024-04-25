# """
# Contains classes and functions to interact with the database and format data responses.
# """

# from flask import jsonify
# import sqlite3
# from dataclasses import dataclass, field, asdict
# from typing import List

# from controller import DATABASE_FILE

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
# # Query Functions
# ###

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

# def insert_hero(data):

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


# def remove_hero(id):
   
#     conn = sqlite3.connect(DATABASE_FILE)
#     cur = conn.cursor()
#     cur.execute('DELETE FROM heroes WHERE hero_id = ?', (id,))
#     conn.commit()
#     return {'success':True}


import psycopg2
from controller import *

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
    except Exception as e:
        print(f"Error in select_all_heroes: {str(e)}")
        return []

def select_all_powers(limit):
    try:
        conn = psycopg2.connect(c**db_params)
        cur = conn.cursor()
        cur.execute('SELECT * FROM powers LIMIT %s', (limit,))
        results = cur.fetchall()
        powers = []
        for result in results:
            power = Power(result[1], result[3], result[2], result[0])
            powers.append(power)
        return powers
    except Exception as e:
        print(f"Error in select_all_powers: {str(e)}")
        return []

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
    except Exception as e:
        print(f"Error in select_hero: {str(e)}")
        return None

def select_power(id):
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute('SELECT * FROM powers WHERE power_id = %s', (id,))
        result = cur.fetchone()
        if result is None:
            return None
        power = Power(result[1], result[3], result[2], result[0])
        return power
    except Exception as e:
        print(f"Error in select_power: {str(e)}")
        return None

def select_hero_powers(hero_id):
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute('SELECT hero_name FROM heroes WHERE hero_id = %s', (hero_id,))
        hero_result = cur.fetchone()

        if hero_result:
            hero_name = hero_result[0]
        else:
            return "Hero not found", []

        cur.execute('''
            SELECT p.power_name, p.power_level, p.power_type, p.power_id
            FROM heroes AS h
            JOIN heroes_powers AS hp ON h.hero_id = hp.hero_id
            JOIN powers AS p ON hp.power_id = p.power_id
            WHERE h.hero_id = %s
            ''',
            (hero_id,))
        power_results = cur.fetchall()
        powers = []

        for result in power_results:
            power = Power(result[0], result[1], result[2], result[3])
            powers.append(power)

        return hero_name, powers
    except Exception as e:
        print(f"Error in select_hero_powers: {str(e)}")
        return "Error", []

def insert_hero(data):
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO heroes (hero_name, gender, eye_color, species, hair_color, height, weight, publisher, skin_color, alignment)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING hero_id
            ''',
            (data.get('hero_name', ''),
            data.get('gender', ''),
            data.get('eye_color', ''),
            data.get('species', ''),
            data.get('hair_color', ''),
            data.get('height', 0.0),
            data.get('weight', 0.0),
            data.get('publisher', ''),
            data.get('skin_color', ''),
            data.get('alignment', ''))
        )
        hero_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Hero added successfully", "hero_id": hero_id}, 201
    except Exception as e:
        print(f"Error in insert_hero: {str(e)}")
        return {"error": "Failed to add hero"}, 500

def modify_hero(hero_id, data):
    try:
        conn = psycopg2

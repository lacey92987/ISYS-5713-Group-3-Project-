from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import sqlite3
from pathlib import Path

app = Flask(__name__) 
CORS(app)
DB_PATH = Path.cwd() 
DATABASE_FILE = DB_PATH / 'database.db'



# GET - at least one for every table (except mapping tables)

# Get all (must have a filter) LIMIT
@app.get(/heroes?limit=10)
def select_all_heros():
    
    print(DATABASE_FILE)
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    # Get column names from the sales table
    cur.execute('SELECT * FROM heroes LIMIT 10')
    return cur.fetchall()
    
@app.get(/powers?limit=10)
def select_all_powers():
    
    print(DATABASE_FILE)
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    # Get column names from the sales table
    cur.execute('SELECT * FROM powers LIMIT 10')
    return cur.fetchall()

@app.get(/powers_basic?limit=10)
def select_all_powers_basic():
    
    print(DATABASE_FILE)
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    # Get column names from the sales table
    cur.execute('SELECT * FROM powers_basic LIMIT 10')
    return cur.fetchall()

@app.get(/heroes_powers?limit=10)
def select_all_heros_powers():
    
    print(DATABASE_FILE)
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    # Get column names from the sales table
    cur.execute('SELECT * FROM heroes_powers LIMIT 10')
    return cur.fetchall()

# Get one by one
@app.get(/heroes/{id})
def select_heroes(id):
   
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM heroes WHERE hero_id = ?', (id,))
    return cur.fetchone() 

@app.get(/powers/{id})
def select_powers(id):
    
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    # Get column names from the sales table
    cur.execute('SELECT * FROM powers WHERE power_id = ?', (id,))
    return cur.fetchone() 

# Get that spans multiple tables (Heroes/powers/heroes_powers)
@app.get(/)
def select_heroes_powers:

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cur.execute('''SELECT h.hero_name as "Name", p.power_name as "Power"
    FROM heroes AS h
    JOIN heroes_powers.heroes_powers AS hp ON h.hero_id = hp.hero_id
    JOIN powers.powers AS p ON hp.power_id = p.power_id;
''')
    return cur.fetchall()

# POST - Create a new entity for your database (can be a single table or multiple tables)
@app.route('/heroes', methods=['POST'])
def post_hero():

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
   
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute('DELETE FROM heroes WHERE HeroId = ?', (id,))
    conn.commit()
    return {'success':True}

   
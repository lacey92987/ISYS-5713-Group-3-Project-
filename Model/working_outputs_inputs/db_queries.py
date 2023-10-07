# import sqlite3
# import os
# from pathlib import Path
# data_folder = Path("C:\\Users\\lacey\\OneDrive\\Documents\\GitHub\\ISYS-5713-Group-3-Project-\\Model\\working_outputs_inputs")

# # Set the database filename
# db_file =data_folder/"heroes.db"

# cnn = sqlite3.connect(db_file)
# cur = cnn.cursor()
# query = 'SELECT "publisher", "hero_name" from heroes group by "publisher"'
# results = cur.execute(query).fetchall()
# print(results)
# cnn.close()


import sqlite3
import pandas as pd
from pathlib import Path

#data_folder = Path("C:\\Users\\lacey\\OneDrive\\Documents\\GitHub\\ISYS-5713-Group-3-Project-\\Model\\working_outputs_inputs")

import sqlite3
import os
import pandas as pd
# Set the directory where your databases are located
db_directory = 'C:\\Users\\OneDrive\\Documents\\GitHub\\ISYS-5713-Group-3-Project-\\Model\\working_outputs_inputs'

# Specify the main database filename
db_filename = 'heroes.db'

# Create the full path to the main database
db_file = os.path.join(db_directory, db_filename)
print("Database File Path:", db_file)
# Create a connection to the main database
conn = sqlite3.connect(db_file)

# Attach other databases from the same directory
cursor = conn.cursor()

# Attach the heroes_powers database from the same directory
heroes_powers_db_filename = 'heroes_powers.db'
cursor.execute(f"ATTACH DATABASE '{os.path.join(db_directory, heroes_powers_db_filename)}' AS heroes_powers;")

# Attach the powers database from the same directory
powers_db_filename = 'powers.db'
cursor.execute(f"ATTACH DATABASE '{os.path.join(db_directory, powers_db_filename)}' AS powers;")

# Define your SQL query for the JOIN operation
query = '''
    SELECT h.hero_name as "Name", p.power_name as "Power"
    FROM heroes AS h
    JOIN heroes_powers.heroes_powers AS hp ON h.hero_id = hp.hero_id
    JOIN powers.powers AS p ON hp.power_id = p.power_id;
'''

# Execute the query and fetch the results into a DataFrame
data = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Group powers by hero name and aggregate them as a list
grouped_data = data.groupby("Name")["Power"].agg(list).reset_index()

# Print the grouped data
grouped_data


import sqlite3
import pandas as pd

# Set the directory where your databases are located
db_directory = 'C:\\Users\\OneDrive\\Documents\\GitHub\\ISYS-5713-Group-3-Project-\\Model\\working_outputs_inputs'

# Specify the main database filename
db_filename = 'heroes.db'

# Create the full path to the main database
db_file = os.path.join(db_directory, db_filename)
print("Database File Path:", db_file)
# Create a connection to the main database
conn = sqlite3.connect(db_file)

# Attach other databases from the same directory
cursor = conn.cursor()

# Attach the heroes_powers database from the same directory
heroes_powers_db_filename = 'heroes_powers.db'
cursor.execute(f"ATTACH DATABASE '{os.path.join(db_directory, heroes_powers_db_filename)}' AS heroes_powers;")

# Attach the powers database from the same directory
powers_db_filename = 'powers.db'
cursor.execute(f"ATTACH DATABASE '{os.path.join(db_directory, powers_db_filename)}' AS powers;")

# Define your SQL query with JOIN operations and sum power_level
query = '''
    SELECT h.hero_name as "Name", sum(p.power_level) as "Total Power Level"
    FROM heroes AS h
    JOIN heroes_powers.heroes_powers AS hp ON h.hero_id = hp.hero_id
    JOIN powers.powers AS p ON hp.power_id = p.power_id
    GROUP BY h.hero_name;
'''

# Execute the query and fetch the results
data = pd.read_sql_query(query, cnn)

# Close the database connection
cnn.close()

# Print the query itself for debugging
print("SQL Query:")
print(query)

# Print the data
print("Data:")
print(data)
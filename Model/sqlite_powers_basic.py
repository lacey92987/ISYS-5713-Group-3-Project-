#code for uploading data into database
import sqlite3
from pathlib import Path

# Define the path to the data folder
data_folder = Path("C:\\Users\\lacey\\OneDrive\\Documents\\GitHub\\ISYS-5713-Group-3-Project-\\Model\\working_outputs_inputs")

# Set the database filename
db_filename = data_folder / "powers_basic.db"

# Set the data filename
data_filename = data_folder / "powers_basic.csv"

# Create the database connection
conn = sqlite3.connect(db_filename)

# Create a cursor object
cur = conn.cursor()

# Drop the table if it exists
cur.execute("DROP TABLE IF EXISTS powers_basic")

# Create the table with the correct column names and data types
cur.execute("CREATE TABLE powers_basic (power_id INTEGER, power_name TEXT)")

# Load data from the CSV file
with open(data_filename, 'r') as file:
    # Skip the header row
    next(file)
    for line in file:
        # Split each line into values and insert into the table
        row = line.strip().split(',')
        cur.execute("INSERT INTO powers_basic VALUES (?, ?)", (int(row[0]), row[1]))

    # Commit the changes inside the 'with' block
    conn.commit()

# Select all rows from the table and print the result
cur.execute("SELECT * FROM powers_basic")
print(cur.fetchall())

# Close the cursor and the connection
cur.close()
conn.close()
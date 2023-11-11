from pathlib import Path

###
# Configuration
###

# Define the path to the 'data' folder
DATA_FOLDER = Path('data')

# Set the output database filename
DATABASE_FILE = DATA_FOLDER / 'database.db'

HEROES_FILENAME = DATA_FOLDER / 'heroes.csv'
POWERS_FILENAME = DATA_FOLDER / 'powers.csv'
HEROES_POWERS_FILENAME = DATA_FOLDER / 'heroes_powers_convert.csv'
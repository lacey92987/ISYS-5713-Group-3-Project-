# Code to clean and transform data
# From source files heroes_information.csv and super_hero_powers.csv
# Into dataframes to be loaded into sqlite database

# outputs:

# heroes (dataframe)
    # data for Superhero database table

# heroes_powers (dataframe)
    # data for Hero_Power linking table

# powers_basic (dataframe)
    # basic data for Superpower data table (power_id, power_name)

# powers_basic.csv (CSV file)
    # to be copied manually into ChatGPT to add power_type and power_level columns

# heroes.csv and heroes_powers.csv (CSV files)
    # for checking results



import pandas as pd
from pathlib import Path



# specify the source_data and working_outputs directory
source_data = Path('Model/source_data')
working = Path('Model/working_outputs_inputs')


# Read in and clean the heroes data

# read in the heroes_information data
with open(source_data / 'heroes_information.csv') as f:
    heroes = pd.read_csv(f)

# create unique ids in the heroes table
heroes['hero_id'] = range(1, len(heroes) + 1)

# standardize column names and rename race to species
heroes = heroes.rename(columns={'name': 'hero_name', 'Gender': 'gender','Eye color': 'eye_color','Race': 'species','Hair color': 'hair_color', 'Height': 'height', 'Publisher': 'publisher', 'Skin color': 'skin_color', 'Alignment': 'alignment', 'Weight': 'weight'})

# reorder the columns and drop the unnamed column
heroes = heroes[['hero_id','hero_name','gender','eye_color','species','hair_color','height','weight','publisher','skin_color','alignment']]

# replace values '-' with null
heroes = heroes.replace(to_replace='-', value=None, regex=False)



# read in the raw powers data
with open(source_data / 'super_hero_powers.csv') as f:
    powers_raw = pd.read_csv(f)



# create the powers table from the raw data column names

# get all the columns except hero_names
powers_basic = powers_raw.drop(columns=['hero_names'])
powers_basic = powers_basic.columns.to_frame(index=False)
powers_basic = powers_basic.rename(columns={0: 'power_name'})

# create unique ids in the powers table
powers_basic['power_id'] = range(1, len(powers_basic) + 1)

# reorder the columns
powers_basic = powers_basic[['power_id', 'power_name']]



# transform powers_raw to create the basic heroes_powers linking table

# unpivot powers_raw to create the many-to-many linking table
heroes_powers = powers_raw.melt(id_vars=['hero_names'], var_name='power_name', value_name='has_power')

# rename hero_names to hero_name for consistency
heroes_powers = heroes_powers.rename(columns={'hero_names': 'hero_name'})

# filter to rows where has_power == True
heroes_powers = heroes_powers[heroes_powers['has_power'] == True]
heroes_powers = heroes_powers.drop(columns=['has_power'])



# look up foreign keys and clean the to finalize the heroes_powers linking table

# look up hero_id from the hero_name
heroes_powers = heroes_powers.merge(heroes[['hero_id','hero_name']], how='left', on='hero_name')

# look up power_id from the powers_basic table
heroes_powers = heroes_powers.merge(powers_basic[['power_id','power_name']], on='power_name')

# sort by hero_name
heroes_powers = heroes_powers.sort_values(by='hero_name')

# drop rows with missing hero_id or power_id
heroes_powers = heroes_powers.dropna(subset=['hero_id','power_id'])

# drop hero_name and power_name
heroes_powers = heroes_powers.drop(columns=['hero_name','power_name'])



# export the powers_basic table to CSV for further processing in ChatGPT
powers_basic.to_csv(working / 'powers_basic.csv', index=False)



# export the heroes and heroes_powers tables to CSV to check results
heroes.to_csv(working / 'heroes.csv', index=False)
heroes_powers.to_csv(working / 'heroes_powers.csv', index=False)
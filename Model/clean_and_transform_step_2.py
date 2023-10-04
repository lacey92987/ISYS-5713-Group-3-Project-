# Code to load expanded powers.csv
# Into dataframe to be loaded into sqlite database

# outputs:

# powers (dataframe)
    # data for Superpower database table

import pandas as pd
from pathlib import Path

# specify the working_inputs_outputs directory
working = Path('Model/working_outputs_inputs')

# read in the powers data
with open(working / 'powers.csv') as f:
    powers = pd.read_csv(f)

#sort powers by power_type and power level
powers = powers.sort_values(by=['power_type','power_level'], ascending=[True,False])
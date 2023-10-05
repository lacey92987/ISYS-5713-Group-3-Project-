import csv
import sqlite3
from pathlib import Path
data_folder = Path("C:\\Users\\lacey\\OneDrive\\Documents\\GitHub\\ISYS-5713-Group-3-Project-\\Model\\working_outputs_inputs")
# Input CSV file and output CSV file
input_file = input_file = 'C:\\Users\\lacey\\OneDrive\\Documents\\GitHub\\ISYS-5713-Group-3-Project-\\Model\\working_outputs_inputs\\heroes_powers.csv'

output_file = 'heroes_powers_convert.csv'

# Open the input CSV file for reading and the output CSV file for writing
with open(input_file, 'r') as csv_input, open(output_file, 'w', newline='') as csv_output:
    # Create CSV reader and writer objects
    csv_reader = csv.reader(csv_input)
    csv_writer = csv.writer(csv_output)

    # Write the header row to the output CSV file (if needed)
    header = next(csv_reader)
    csv_writer.writerow(header)

    # Iterate through the rows in the input CSV file
    for row in csv_reader:
        # Convert the value in row 0 from string to float and then to an integer
        try:
            float_value = float(row[0])
            int_value = int(float_value)
            row[0] = str(int_value)  # Update the value in row 0
        except ValueError:
            # Handle cases where the conversion is not possible
            # You can choose to skip the row, log an error, or handle it as needed
            print(f"Error converting {row[0]} to an integer. Skipping row.")
            continue

        # Write the modified row to the output CSV file
        csv_writer.writerow(row)

print(f"Conversion completed. Data written to {output_file}.")

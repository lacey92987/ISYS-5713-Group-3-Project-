import csv
import json

def csv_to_json(csv_filepath, json_filepath):
    data = []
    # Read CSV file and convert it to a list of dictionaries
    with open(csv_filepath, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Convert height and weight to float, handling the special case values
            row['height'] = float(row['height']) if row['height'] != '-99.0' else None
            row['weight'] = float(row['weight']) if row['weight'] != '-99.0' else None
            data.append(row)
    
    # Write the data to a JSON file
    with open(json_filepath, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage:
csv_to_json('heroes.csv', 'heroes.json')





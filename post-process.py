import sys
import os
import json

# Define the folder to loop through from command line arguments
folder_path = sys.argv[1]

# Define the output file name
output_file = "scraped.txt"

# Loop through the folders in the root folder
for folder in os.listdir(folder_path):
    folder_full_path = os.path.join(folder_path, folder)

    # If the folder is not a directory, skip it
    if not os.path.isdir(folder_full_path):
        continue

    # Loop through the files in the folder
    for file_name in os.listdir(folder_full_path):
        file_full_path = os.path.join(folder_full_path, file_name)

        # If the file is not a json file, skip it
        if not file_name.endswith(".json"):
            continue

        # Load the json file
        with open(file_full_path, "r") as f:
            data = json.load(f)

        # Loop through the entries and look for the "Secret" key
        for entry in data:
            if "Secret" in entry and entry["Secret"].startswith("sk-"):
                # Append the value of the "Secret" key to the output file
                with open(output_file, "a") as f:
                    f.write(entry["Secret"] + "\n")

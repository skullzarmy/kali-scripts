import os
import json
import sys

def find_json_files(folder_path):
    json_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files

def concatenate_json_files(json_files, output_file_path):
    master_json = {}
    for file_path in json_files:
        with open(file_path) as f:
            file_content = json.load(f)
            master_json.update(file_content)
    with open(output_file_path, "w") as f:
        f.write(json.dumps(master_json, indent=4))

if __name__ == "__main__":
    folder_path = sys.argv[1]
    json_files = find_json_files(folder_path)
    output_file_path = os.path.join(folder_path, "concat_json.json")
    concatenate_json_files(json_files, output_file_path)

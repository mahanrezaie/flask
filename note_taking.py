import json
import yaml
import os

def read_json(data):
    content = json.loads(data)
    return content

def list_directory(directory):
    files_dict = {}
    files = os.listdir(directory)
    for i, file in enumerate(files):
        files_dict[str(i+1)] = file

    return files_dict
            
def json_dump(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent= 4)

    

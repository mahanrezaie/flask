import json
import yaml
import os
from datetime import datetime


def get_timestamp():
    return datetime.now().strftime("%Y%m%d-%H:%M:%S")


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


def check_list_exist():
    if not os.path.exists("notes-list.json"):
        with open("notes-list.json", "w") as f:
            json.dump({}, f, indent=4)  # creates an empty JSON object
   
def json_load(file):
        with open(file, "r") as f:
            data = json.load(f)
        return(data)
    
def tag_exists(tag, notes):
    return any(note["file_name"] == f"{tag}.json" for note in notes.values())

def tag_exists(tag, notes):
    for note in notes.values():
        if note["file_name"] == f"{tag}.json":
            return True
    return False


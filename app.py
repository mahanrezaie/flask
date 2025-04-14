from flask import Flask, request
from note_taking import json_load, check_list_exist, tag_exists, get_timestamp, json_dump
import json

app = Flask(__name__)


@app.route("/add", methods=["POST"])
def add():
    check_list_exist()
    user_post = request.json # getting user payload
    list_content = json_load("notes-list.json")

    if user_post is None or "id" not in user_post:
        return "Invalid JSON: missing 'id'", 400
    elif user_post["id"] in  list_content:
        return "Invalid Json: this 'id' exists", 400

    current_timestamp = get_timestamp()
    user_post["created_at"] = current_timestamp

    #check to see if note with this tag exists.
    if tag_exists(user_post["tag"], list_content):
        return "Invalid Json: similar 'tag' exists", 400
    else:
        note_file = f"json_notes/{user_post["tag"]}.json"

    # Save the full note in a file
    json_dump(user_post, note_file)

    # Update notes-list.json (append the id and note path)
    with open("notes-list.json", "r") as f:
        notes_list = json.load(f)

    notes_list[user_post["id"]] = {

        "file_name": f"{user_post["tag"]}.json",
        "has_yaml": False
    }

    with open("notes-list.json", "w") as f:
        json.dump(notes_list, f, indent=4)

    return "Note added :)", 200


@app.route("/list", methods=["GET"])
def list():
    list_content = json_load("notes-list.json")
    return list_content, 200

@app.route("/delete/<note_id>", methods=["DELETE"])
def delete(note_id: str):
    list_content = json_load("notes-list.json")
    if note_id not in list_content:
        return f"note {note_id} does not exists", 400

@app.route("/update/<note_id>", methods=["PUT"])
def update(note_id):
    list_content = json_load("notes-list.json")
    if note_id not in list_content:
        return f"note {note_id} does not exists", 400


@app.route("/get-note/<note_id>", methods=["GET"])
def get_note(note_id: str):
    list_content = json_load("notes-list.json")
    if note_id not in list_content:
        return f"note {note_id} does not exists", 404
    else:
        content = json_load(f"notes/{list_content[note_id]["file_name"]}")
        return content, 200
        
        

@app.route("/export", methods=["GET"])
def export():
    return f"hello"


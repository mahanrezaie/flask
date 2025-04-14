from flask import Flask, request
from note_taking import json_load, check_list_exist, read_json, get_timestamp, list_directory, json_dump
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

    note_file = f"notes/{current_timestamp}.json"

    # Save the full note in a file
    json_dump(user_post, note_file)

    # Update notes-list.json (append the id and note path)
    with open("notes-list.json", "r") as f:
        notes_list = json.load(f)

    notes_list[user_post["id"]] = note_file

    with open("notes-list.json", "w") as f:
        json.dump(notes_list, f, indent=4)

    return "Note added :)"


@app.route("/list", methods=["GET"])
def list():
    content = list_directory("notes")
    json_dump(content, "notes-list.json") # save files with id in notes-list
    return content

@app.route("/delete/<note_id>", methods=["DELETE"])
def delete():
    return f"hello"

@app.route("/update/<note_id>", methods=["PUT"])
def update():
    return f"hello"

@app.route("/get-note/<note_id>", methods=["GET"])
def get_note():
    return f"hello"

@app.route("/export", methods=["GET"])
def export():
    return f"hello"


from flask import Flask, request
import os
from note_taking import find_key_changes, json_load, validate_note_json, check_list_exist, tag_exists, get_timestamp, json_dump, find_key_changes, delete_file, json_to_yaml
import json
import copy

app = Flask(__name__)

@app.route("/add", methods=["POST"])
def add():
    check_list_exist()
    user_post = request.json # getting user payload
    
    # check the structure
    validation, error = validate_note_json(user_post)
    if validation == False:
        return error, 400

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

    notes_list[user_post["id"]] =  f"{user_post["tag"]}.json"
    

    with open("notes-list.json", "w") as f:
        json.dump(notes_list, f, indent=4)

    return "Note added :)", 200


@app.route("/list", methods=["GET"])
def list():
    check_list_exist()
    list_content = json_load("notes-list.json")
    return list_content, 200

@app.route("/delete/<note_id>", methods=["DELETE"])
def delete(note_id: str):
    list_content = json_load("notes-list.json")
    if note_id not in list_content:
        return f"note {note_id} does not exists", 404
    else:
        file_name = list_content[note_id]
        delete_file(f"json_notes/{file_name}")
        del list_content[note_id]
        json_dump(list_content, "notes-list.json")
        return "note deleted :]" , 200

    
@app.route("/update/<note_id>", methods=["PUT"])
def update(note_id):
    # open note
    user_put = request.get_json()
    list_content = json_load("notes-list.json")
    if note_id not in list_content:
        return f"note {note_id} does not exists", 404

    file_name = list_content[f"{note_id}"]
    note_data = json_load(f"json_notes/{file_name}")


    keys_to_compare = [
        "id",
        "field",
        "content",
        "tag"
    ]
    different_keys = find_key_changes(note_data, user_put, keys_to_compare)

    validate, error = validate_note_json(user_put)
    if validate == False:
        return error, 400

    if len(different_keys) == 0 :
        return f" nothing to update.", 404

    #update id if user wants
    if user_put["id"] != note_id:
        del list_content[note_id]
        list_content[user_put["id"]] = f"{user_put["tag"]}.json"
        json_dump(list_content, "")





    timestamp = get_timestamp()
    # select created_at from json
    created_at = note_data["created_at"]
    user_put["created_at"] = created_at
    user_put["update_at"] = timestamp

    # History handle

    #check if history does not exist add it to the user_put
    if "history" not in note_data:
        user_put["history"] = {}
    else:
        # used deepcopy to avoid conflict between old and upadted versions
        user_put["history"] = copy.deepcopy(note_data["history"])

    user_put["history"][timestamp] = {
        "changes": different_keys,
        "old_version": f"history/{file_name}{timestamp}.json"
    }
    json_dump(note_data, f"history/{file_name}{timestamp}.json")
    json_dump(user_put, f"json_notes/{file_name}")
    return f"Updated succesfully :)"

@app.route("/get-note/<note_id>", methods=["GET"])
def get_note(note_id):
    list_content = json_load("notes-list.json")
    if note_id not in list_content:
        return f"note {note_id} does not exists", 404
    else:
        content = json_load(f"json_notes/{list_content[note_id]}")
        return content, 200
        
@app.route("/export", methods=["GET"])
def export():
    list_content = json_load("notes-list.json")  
    file_names = [value for value in list_content.values()]
    clean_files = [f.removesuffix(".json") for f in file_names]


    exported = 0
    skipped = 0

    for name in clean_files:
        json_file_path = f"json_notes/{name}.json"
        yaml_file_path = f"yaml_notes/{name}.yaml"

        if os.path.exists(yaml_file_path):
            skipped += 1
            continue  # Skip if YAML already exported

        if os.path.exists(json_file_path):
            with open(json_file_path, "r") as f:
                json_data = f.read()
                json_to_yaml(json_data, yaml_file_path)
                exported += 1

    return {
        "exported": exported,
        "skipped_existing": skipped,
        "total_notes": len(clean_files)
    }, 200

if __name__ == "__main__":
    app.run(debug=True)


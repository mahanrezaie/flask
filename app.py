from flask import Flask
from note_taking import read_json
import os

app = Flask(__name__)


@app.route("/add", methods=["POST"])
def add():
    return f"This is add route"

@app.route("/list", methods=["GET"])
def list():
    content = os.listdir("notes")
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


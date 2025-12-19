from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

FILE = "students.json"

# Create file if not exists
if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        json.dump([], f)

def read_data():
    with open(FILE, "r") as f:
        return json.load(f)

def write_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(read_data())

@app.route("/students", methods=["POST"])
def add_student():
    data = read_data()
    data.append({
        "name": request.json["name"],
        "present": 0,
        "total": 0
    })
    write_data(data)
    return jsonify({"message": "Student added"})

@app.route("/attendance/<int:index>", methods=["POST"])
def mark_attendance(index):
    data = read_data()
    status = request.json["status"]

    data[index]["total"] += 1
    if status == "present":
        data[index]["present"] += 1

    write_data(data)
    return jsonify({"message": "Attendance marked"})

# REQUIRED for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
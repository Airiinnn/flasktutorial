from flask import Flask, jsonify, render_template, request
import csv

app = Flask(__name__)

PEOPLE = []
with open("registrants.csv", "r") as file:
    for line in file.readlines():
        PEOPLE.append(line.rstrip())

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registered", methods=["POST"])
def register():
    if not request.form.get("name") or not request.form.get("classid"):
        return render_template("failure.html")
    else:
        file = open("registrants.csv", "a")
        writer = csv.writer(file)
        writer.writerow((request.form.get("name"), request.form.get("classid")))
        file.close()
        PEOPLE.append("{},{}".format(request.form.get("name"), request.form.get("classid")))
        return render_template("success.html")

@app.route("/registrants")
def registants():
    return render_template("registrants.html")

@app.route("/registrants/search")
def search():
    q = request.args.get("q")
    if q == "":
        persons = [person for person in PEOPLE]
        return jsonify(persons)
    else:
        persons = [person for person in PEOPLE if q and person.startswith(q)]
        return jsonify(persons)
from flask import Blueprint, jsonify
from sqlite3 import connect


app = Blueprint("medicine", __name__, url_prefix="/medicine")


@app.route("/all")
def medicine_list():
    with connect("main.db") as conn:
        c = conn.cursor()
        c.execute("SELECT id, name FROM medicine;")
        rows = c.fetchall()
    medicines = [{"id": r[0], "name": r[1]} for r in rows]
    return jsonify(medicines)


@app.route("/<int:id>")
def medicine_detail(id):
    with connect("main.db") as conn:
        c = conn.cursor()
        c.execute("SELECT id, name FROM medicine WHERE id = ?", (id,))
        row = c.fetchone()
    if row is None:
        return jsonify({"error": "not found"}), 404
    id_, name = row
    return jsonify({"id": id_, "name": name})

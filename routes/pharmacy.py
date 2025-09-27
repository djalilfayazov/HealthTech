from flask import Blueprint, jsonify
from sqlite3 import connect


app = Blueprint("pharmacy", __name__, url_prefix="/pharmacy")


@app.route("/all")
def pharmacy_list():
    with connect("main.db") as conn:
        c = conn.cursor()
        c.execute("SELECT id, name, address, phone FROM pharmacy;")
        rows = c.fetchall()
    pharmacies = [
        {"id": r[0], "name": r[1], "address": r[2], "phone": r[3]}
        for r in rows
    ]
    return jsonify(pharmacies)


@app.route("/<int:id>")
def pharmacy_detail(id):
    with connect("main.db") as conn:
        c = conn.cursor()
        c.execute(
            "SELECT id, name, address, phone FROM pharmacy WHERE id = ?",
            (id,)
        )
        row = c.fetchone()
    if row is None:
        return jsonify({"error": "Pharmacy not found"}), 404

    pharmacy = {
        "id": row[0],
        "name": row[1],
        "address": row[2],
        "phone": row[3]
    }
    return jsonify(pharmacy)


@app.route("/search/name/<string:name>")
def pharmacy_search_name(name):
    pattern = f"%{name}%"
    with connect("main.db") as conn:
        c = conn.cursor()
        c.execute(
            """
            SELECT id, name, address, phone
            FROM pharmacy
            WHERE LOWER(name) LIKE LOWER(?)
            """,
            (pattern,)
        )
        rows = c.fetchall()
    pharmacies = [
        {"id": r[0], "name": r[1], "address": r[2], "phone": r[3]}
        for r in rows
    ]
    return jsonify(pharmacies)


@app.route("/search/phone/<string:phone>")
def pharmacy_search_phone(phone):
    with connect("main.db") as conn:
        c = conn.cursor()
        c.execute(
            """
            SELECT id, name, address, phone
            FROM pharmacy
            WHERE phone LIKE ?
            """,
            (f"%{phone}%",)
        )
        rows = c.fetchall()
    pharmacies = [
        {"id": r[0], "name": r[1], "address": r[2], "phone": r[3]}
        for r in rows
    ]
    return jsonify(pharmacies)

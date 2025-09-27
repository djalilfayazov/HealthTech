from flask import Blueprint, jsonify, request
from sqlite3 import connect
import re


app = Blueprint("inventory", __name__, url_prefix="/inventory")


def _norm(s):
    return re.sub(r'[\W_]+', '', s.casefold(), flags=re.UNICODE) if s else ""


@app.route("/search/<name>")
def search_medicine(name):
    sort_field = request.args.get("sort", "").lower()
    sort_dir   = request.args.get("order", "asc").lower()
    if sort_field not in {"price", "amount"}:
        sort_field = "m.name"
        sort_dir   = "asc"
    elif sort_dir not in {"asc", "desc"}:
        sort_dir = "asc"

    pattern = f"%{_norm(name)}%"
    with connect("main.db") as conn:
        conn.create_function("norm", 1, _norm)
        rows = conn.execute(f"""
            SELECT m.name, p.id, p.name, p.address, p.phone, i.amount, i.price
            FROM medicine m
            JOIN inventory i ON m.id = i.medicine_id
            JOIN pharmacy p ON p.id = i.pharmacy_id
            WHERE norm(m.name) LIKE ?
            ORDER BY {sort_field} {sort_dir}, p.name
        """, (pattern,)).fetchall()

    if not rows:
        return jsonify({"message": "No pharmacies found for this medicine"}), 404

    return jsonify([
        {"medicine": r[0], "pharmacy_id": r[1], "pharmacy": r[2],
         "address": r[3], "phone": r[4], "amount": r[5], "price": float(r[6])}
        for r in rows
    ])

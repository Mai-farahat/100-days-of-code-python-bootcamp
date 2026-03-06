from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import os
import shutil

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "cafes.db")

# Copy source DB if not already present
if not os.path.exists(DB_PATH):
    shutil.copy("/mnt/user-data/uploads/cafes.db", DB_PATH)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ─── Page Routes ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


# ─── API Routes ─────────────────────────────────────────────────────────────

@app.route("/api/cafes", methods=["GET"])
def get_cafes():
    location = request.args.get("location", "")
    wifi     = request.args.get("wifi", "")
    sockets  = request.args.get("sockets", "")

    conn = get_db()
    query = "SELECT * FROM cafe WHERE 1=1"
    params = []

    if location:
        query += " AND location = ?"
        params.append(location)
    if wifi == "1":
        query += " AND has_wifi = 1"
    if sockets == "1":
        query += " AND has_sockets = 1"

    query += " ORDER BY name ASC"
    cafes = [dict(r) for r in conn.execute(query, params).fetchall()]
    conn.close()
    return jsonify(cafes)


@app.route("/api/locations", methods=["GET"])
def get_locations():
    conn = get_db()
    locs = [r[0] for r in conn.execute("SELECT DISTINCT location FROM cafe ORDER BY location").fetchall()]
    conn.close()
    return jsonify(locs)


@app.route("/api/cafes", methods=["POST"])
def add_cafe():
    data = request.json
    required = ["name", "map_url", "img_url", "location", "has_sockets",
                "has_toilet", "has_wifi", "can_take_calls"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    conn = get_db()
    conn.execute(
        """INSERT INTO cafe (name, map_url, img_url, location, has_sockets,
           has_toilet, has_wifi, can_take_calls, seats, coffee_price)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (data["name"], data["map_url"], data["img_url"], data["location"],
         int(data["has_sockets"]), int(data["has_toilet"]), int(data["has_wifi"]),
         int(data["can_take_calls"]), data.get("seats", ""), data.get("coffee_price", ""))
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Cafe added!"}), 201


@app.route("/api/cafes/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    conn = get_db()
    result = conn.execute("DELETE FROM cafe WHERE id = ?", (cafe_id,))
    conn.commit()
    conn.close()
    if result.rowcount == 0:
        return jsonify({"error": "Cafe not found"}), 404
    return jsonify({"success": True, "message": "Cafe deleted"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
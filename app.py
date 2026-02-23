from flask import Flask, jsonify, request
import sqlite3, os, shutil, time
from config import DB_PATH

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

QUARANTINE_DIR = os.path.join(BASE_DIR, "quarantine")
os.makedirs(QUARANTINE_DIR, exist_ok=True)


# ================= EVENTS API =================
@app.route("/api/events")
def get_events():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM events ORDER BY timestamp DESC LIMIT 100")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)


# ================= QUARANTINE API =================
@app.route("/quarantine", methods=["POST"])
def quarantine_file():

    data = request.get_json()
    path = data.get("path")

    print("REQUESTED PATH:", path)

    if not path:
        return jsonify({"status": "fail", "error": "No path provided"})

    path = os.path.abspath(os.path.normpath(path))

    if not os.path.exists(path):
        return jsonify({"status": "fail", "error": "File not found", "path": path})

    filename = os.path.basename(path)
    timestamp = str(int(time.time()))
    dest = os.path.join(QUARANTINE_DIR, f"{timestamp}_{filename}")

    try:
        # MOVE (safer than copy+delete)
        shutil.move(path, dest)

        print("MOVED TO:", dest)

        return jsonify({
            "status": "ok",
            "message": "File quarantined",
            "destination": dest
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"status": "fail", "error": str(e)})


# ================= FRONTEND =================
@app.route("/")
def home():
    return open("templates/index.html").read()


# ================= RUN =================
if __name__ == "__main__":
    app.run(port=5001, debug=True)

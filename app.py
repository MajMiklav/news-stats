from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import Counter
import os

app = Flask(__name__)
# Odpri CORS za vse poti in metode
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=False)


@app.after_request
def add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return resp

# In-memory statistika (reset ob restartu)
total_events = 0
events_per_location = Counter()

@app.route("/", methods=["GET"])
def health():
    return jsonify({"ok": True})

# Glavni stats endpoint
@app.route("/stats", methods=["GET"])
def get_stats():
    return jsonify({
        "totalEvents": total_events,
        "eventsPerLocation": dict(events_per_location)
    })

# Alias, ker frontend kliče /summary
@app.route("/summary", methods=["GET"])
def get_summary():
    return get_stats()

# Sprejem dogodkov
@app.route("/stats", methods=["POST", "OPTIONS"])
def add_event():
    if request.method == "OPTIONS":
        return ("", 204)
    global total_events, events_per_location
    data = request.get_json(force=True, silent=True) or {}
    location = (data.get("location") or "Neznano").strip() or "Neznano"
    total_events += 1
    events_per_location[location] += 1
    return jsonify({"ok": True, "newTotal": total_events})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8085))  # Render posreduje PORT
    app.run(host="0.0.0.0", port=port)

from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import Counter
import os

app = Flask(__name__)
# Za testiranje dovoli vsem originom
CORS(app)  

# Shramba v RAM-u (reset ob restartu)
total_events = 0
events_per_location = Counter()

@app.route("/", methods=["GET"])
def health():
    return jsonify({"ok": True})

@app.route("/stats", methods=["GET"])
def get_stats():
    return jsonify({
        "totalEvents": total_events,
        "eventsPerLocation": dict(events_per_location)
    })

@app.route("/stats", methods=["POST"])
def add_event():
    global total_events, events_per_location
    data = request.get_json(force=True)
    location = (data.get("location") or "Neznano").strip() or "Neznano"
    total_events += 1
    events_per_location[location] += 1
    return jsonify({"ok": True, "newTotal": total_events})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8085))  # Render poda PORT
    app.run(host="0.0.0.0", port=port)

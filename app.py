from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import Counter
import os

app = Flask(name)
Open CORS for all routes (ok for demo)
CORS(app, resources={r"/": {"origins": ""}}, supports_credentials=False)

@app.after_request
def add_cors_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return resp

In-memory stats (reset on restart)
total_news = 0
news_by_day = Counter()

@app.route("/", methods=["GET"])
def health():
    return jsonify({"ok": True})

@app.route("/summary", methods=["GET"])
def summary():
    top = None
    if news_by_day:
        day, count = max(news_by_day.items(), key=lambda kv: kv[1])
        top = {"day": day, "count": count}
    return jsonify({
        "totalNews": total_news,
        "newsByDay": dict(news_by_day),
        "topDay": top
    })

@app.route("/ingest", methods=["POST", "OPTIONS"])
def ingest():
    if request.method == "OPTIONS":
        # CORS preflight
        return ("", 204)
    global total_news, news_by_day
    data = request.get_json(silent=True) or {}
    date = (data.get("date") or "").strip()
    if not date:
        return jsonify({"error": "date is required (YYYY-MM-DD)"}), 400
    total_news += 1
    news_by_day[date] += 1
    return jsonify({"ok": True, "totalNews": total_news})

if name == "main":
    port = int(os.environ.get("PORT", 8085))
    app.run(host="0.0.0.0", port=port)
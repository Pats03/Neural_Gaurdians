# # app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from auth_utils import hash_password, check_password
import humanize
# Load environment variables
load_dotenv()

# Local imports
from lang_agent import run_agent
from db import incidents_col, users_col,users,admins_col
from ollama_client import generate as ollama_generate

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

PORT = int(os.getenv("PORT", 8000))


# # ------------------------
# # Routes
# # ------------------------
# # @app.route("/isblocked", methods=["POST"])
# # def isblocked():
# #     """
# #     Dummy login endpoint.
# #     Only checks if user is blocked in MongoDB.
# #     """
# #     body = request.get_json(force=True)
# #     username = body.get("username")

# #     if not username:
# #         return jsonify({"error": "Missing username"}), 400

# #     user = users_col.find_one({"username": username})
# #     if user and user.get("status") == "blocked":
# #         return jsonify({
# #             "success": False,
# #             "message": f"User '{username}' is BLOCKED due to high-risk activity."
# #         }), 403

# #     return jsonify({
# #         "success": True,
# #         "message": f"Welcome, {username}! (not blocked)"
# #     }), 200

# @app.route("/incident", methods=["POST"])
# def incident():
#     event = request.get_json(force=True)
#     if not event:
#         return jsonify({"error": "Missing event JSON"}), 400

#     # Inject IP + hour if missing
#     if "ip_address" not in event:
#         event["ip_address"] = request.remote_addr
#     if "hour_of_day" not in event:
#         event["hour_of_day"] = datetime.utcnow().hour

#     result = run_agent(event)
#     return jsonify(result), 200


# @app.route("/incidents", methods=["GET"])
# def get_incidents():
#     """
#     Fetch all incidents from MongoDB.
#     Optional query params:
#       ?limit=10
#       ?risk=high
#     """
#     limit = int(request.args.get("limit", 20))
#     risk_filter = request.args.get("risk")

#     query = {}
#     if risk_filter:
#         query["risk.risk"] = risk_filter

#     docs = incidents_col.find(query).sort("timestamp", -1).limit(limit)
#     results = []
#     for d in docs:
#         d["_id"] = str(d["_id"])  # convert ObjectId to string
#         results.append(d)

#     return jsonify(results), 200


# @app.route("/incidents/<username>", methods=["GET"])
# def get_user_incidents(username):
#     """
#     Fetch incidents for a specific user.
#     Optional query params:
#       ?minutes=60   -> lookback window (default 24h)
#     """
#     minutes = int(request.args.get("minutes", 1440))  # default 24h
#     cutoff = datetime.utcnow() - timedelta(minutes=minutes)

#     docs = incidents_col.find(
#         {"username": username, "timestamp": {"$gte": cutoff}}
#     ).sort("timestamp", -1)

#     results = []
#     for d in docs:
#         d["_id"] = str(d["_id"])
#         results.append(d)

#     return jsonify(results), 200


# @app.route("/stats", methods=["GET"])
# def get_stats():
#     """
#     Return basic system statistics:
#       - total incidents
#       - count in last 24h
#       - count grouped by risk level
#     """
#     total = incidents_col.count_documents({})
#     last24h = datetime.utcnow() - timedelta(hours=24)
#     recent = incidents_col.count_documents({"timestamp": {"$gte": last24h}})

#     pipeline = [{"$group": {"_id": "$risk.risk", "count": {"$sum": 1}}}]
#     risk_counts = {doc["_id"]: doc["count"] for doc in incidents_col.aggregate(pipeline)}

#     return jsonify({
#         "total_incidents": total,
#         "incidents_last_24h": recent,
#         "risk_distribution": risk_counts
#     }), 200

# @app.route("/register", methods=["POST"])
# def register():
#     body = request.get_json(force=True)
#     username = body.get("username")
#     password = body.get("password")

#     if not username or not password:
#         return jsonify({"success": False, "message": "Missing username or password"}), 400

#     if users.find_one({"username": username}):
#         return jsonify({"success": False, "message": "User already exists"}), 409

#     hashed = hash_password(password)
#     users.insert_one({"username": username, "password": hashed, "status": "active"})

#     return jsonify({"success": True, "message": f"User {username} registered"}), 201

# @app.route("/login", methods=["POST"])
# def login():
#     body = request.get_json(force=True)
#     username = body.get("username")
#     password = body.get("password")

#     if not username or not password:
#         return jsonify({"success": False, "message": "Missing username or password"}), 400

#     status_doc = users_col.find_one({"username": username})

#     if status_doc and status_doc.get("status") == "blocked":
#         return jsonify({"success": False, "message": f"User '{username}' is BLOCKED..please contact Admin.."}), 403
    
#     # Step 1: Check in users collection for credentials
#     user = users.find_one({"username": username})

#     if not user:
#         return jsonify({"success": False, "message": "User not found"}), 404

#     # Step 2: Verify password
#     if not check_password(password, user["password"]):
#         return jsonify({"success": False, "message": "Invalid password"}), 401

    

#     # Step 4: Success
#     return jsonify({
#         "success": True,
#         "message": f"Welcome {username}!",
#         "username": username
#     }), 200

# @app.route("/adminregister", methods=["POST"])
# def admin_register():
#     data = request.get_json(force=True)
#     if not data or "username" not in data or "password" not in data:
#         return jsonify({"error": "username and password required"}), 400

#     username = data["username"]
#     password = data["password"]

#     # ✅ Use admins_col here
#     existing_admin = admins_col.find_one({"username": username})
#     if existing_admin:
#         return jsonify({"error": "Username already exists. Use /adminlogin."}), 403


#     hashed_pw = hash_password(password)
#     admin_doc = {
#         "username": username,
#         "password": hashed_pw,
#         "created_at": datetime.utcnow()
#     }
#     admins_col.insert_one(admin_doc)

#     return jsonify({"message": "Admin registered successfully"}), 201


# @app.route("/adminlogin", methods=["POST"])
# def admin_login():
#     data = request.get_json(force=True)
#     if not data or "username" not in data or "password" not in data:
#         return jsonify({"error": "username and password required"}), 400

#     username = data["username"]
#     password = data["password"]

#     # ✅ Use admins_col here
#     admin = admins_col.find_one({"username": username})
#     if not admin:
#         return jsonify({"error": "Invalid username or password"}), 401

#     if not check_password(password, admin["password"]):
#         return jsonify({"error": "Invalid username or password"}), 401

#     return jsonify({"message": "Login successful", "username": username}), 200

# @app.route("/ollama/chat", methods=["POST"])
# def ollama_chat():
#     body = request.get_json(force=True)
#     prompt = body.get("prompt", "")
#     model = body.get("model", "mistral:7b")

#     resp = ollama_generate(prompt, model=model)
#     return jsonify({"response": resp}), 200
# # ------------------------
# # Run server
# # ------------------------

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=PORT, debug=True)
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from datetime import datetime, timedelta
# from dotenv import load_dotenv
# import os
# # import pytz
# # from dateutil.relativedelta import relativedelta
# import humanize
# # Load environment variables
# load_dotenv()

# # Local imports
# from lang_agent import run_agent
# from db import incidents_col, users_col, file_access_col   # ✅ add file_access collection
# from ollama_client import generate as ollama_generate
# from auth_utils import hash_password, check_password

# # Flask app
# app = Flask(__name__)
# CORS(app)

# PORT = int(os.getenv("PORT", 8000))

# -------------------------
# Auth Routes
# -------------------------
# @app.route("/register", methods=["POST"])
# def register():
#     body = request.get_json(force=True)
#     username = body.get("username")
#     password = body.get("password")

#     if not username or not password:
#         return jsonify({"success": False, "message": "Missing username or password"}), 400

#     if users_col.find_one({"username": username}):
#         return jsonify({"success": False, "message": "User already exists"}), 409

#     hashed = hash_password(password)
#     users_col.insert_one({"username": username, "password": hashed, "status": "active"})

#     return jsonify({"success": True, "message": f"User {username} registered"}), 201


# @app.route("/login", methods=["POST"])
# def login():
#     body = request.get_json(force=True)
#     username = body.get("username")
#     password = body.get("password")

#     if not username or not password:
#         return jsonify({"success": False, "message": "Missing username or password"}), 400

#     user = users_col.find_one({"username": username})
#     if not user:
#         return jsonify({"success": False, "message": "User not found"}), 404

#     if user.get("status") == "blocked":
#         return jsonify({"success": False, "message": f"User '{username}' is BLOCKED"}), 403

#     if not check_password(password, user["password"]):
#         return jsonify({"success": False, "message": "Invalid password"}), 401

#     return jsonify({
#         "success": True,
#         "message": f"Welcome {username}!",
#         "username": username
#     }), 200

@app.route("/register", methods=["POST"])
def register():
    body = request.get_json(force=True)
    username = body.get("username")
    password = body.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Missing username or password"}), 400

    if users.find_one({"username": username}):
        return jsonify({"success": False, "message": "User already exists"}), 409

    hashed = hash_password(password)
    users.insert_one({"username": username, "password": hashed, "status": "active"})

    return jsonify({"success": True, "message": f"User {username} registered"}), 201

@app.route("/login", methods=["POST"])
def login():
    body = request.get_json(force=True)
    username = body.get("username")
    password = body.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Missing username or password"}), 400

    status_doc = users_col.find_one({"username": username})

    if status_doc and status_doc.get("status") == "blocked":
        return jsonify({"success": False, "message": f"User '{username}' is BLOCKED..please contact Admin.."}), 403
    
    # Step 1: Check in users collection for credentials
    user = users.find_one({"username": username})

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    # Step 2: Verify password
    if not check_password(password, user["password"]):
        return jsonify({"success": False, "message": "Invalid password"}), 401

    

    # Step 4: Success
    return jsonify({
        "success": True,
        "message": f"Welcome {username}!",
        "username": username
    }), 200

@app.route("/adminregister", methods=["POST"])
def admin_register():
    data = request.get_json(force=True)
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "username and password required"}), 400

    username = data["username"]
    password = data["password"]

    # ✅ Use admins_col here
    existing_admin = admins_col.find_one({"username": username})
    if existing_admin:
        return jsonify({"error": "Username already exists. Use /adminlogin."}), 403


    hashed_pw = hash_password(password)
    admin_doc = {
        "username": username,
        "password": hashed_pw,
        "created_at": datetime.utcnow()
    }
    admins_col.insert_one(admin_doc)

    return jsonify({"message": "Admin registered successfully"}), 201


@app.route("/adminlogin", methods=["POST"])
def admin_login():
    data = request.get_json(force=True)
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "username and password required"}), 400

    username = data["username"]
    password = data["password"]

    # ✅ Use admins_col here
    admin = admins_col.find_one({"username": username})
    if not admin:
        return jsonify({"error": "Invalid username or password"}), 401

    if not check_password(password, admin["password"]):
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": "Login successful", "username": username}), 200

# -------------------------
# Incident Routes
# -------------------------
@app.route("/incident", methods=["POST"])
def incident():
    event = request.get_json(force=True)
    if not event:
        return jsonify({"error": "Missing event JSON"}), 400

    # Inject IP + hour if missing
    if "ip_address" not in event:
        event["ip_address"] = request.remote_addr
    if "hour_of_day" not in event:
        event["hour_of_day"] = datetime.utcnow().hour

    result = run_agent(event)
    return jsonify(result), 200


@app.route("/incidents", methods=["GET"])
def get_incidents():
    limit = int(request.args.get("limit", 20))
    risk_filter = request.args.get("risk")

    query = {"action.action": "block_user"}
    if risk_filter:
        query["risk.risk"] = risk_filter

    docs = incidents_col.find(query).sort("timestamp", -1).limit(limit)
    results = []
    for d in docs:
        d["_id"] = str(d["_id"])
        results.append(d)

    return jsonify(results), 200


@app.route("/incidents/<username>", methods=["GET"])
def get_user_incidents(username):
    minutes = int(request.args.get("minutes", 1440))
    cutoff = datetime.utcnow() - timedelta(minutes=minutes)

    docs = incidents_col.find(
        {"username": username, "timestamp": {"$gte": cutoff}}
    ).sort("timestamp", -1)

    results = []
    for d in docs:
        d["_id"] = str(d["_id"])
        results.append(d)

    return jsonify(results), 200

# -------------------------
# Analytics Routes
# -------------------------
@app.route("/stats", methods=["GET"])
def get_stats():
    total = incidents_col.count_documents({})
    last24h = datetime.utcnow() - timedelta(hours=24)
    recent = incidents_col.count_documents({"timestamp": {"$gte": last24h}})

    pipeline = [{"$group": {"_id": "$risk.risk", "count": {"$sum": 1}}}]
    risk_counts = {doc["_id"]: doc["count"] for doc in incidents_col.aggregate(pipeline)}

    return jsonify({
        "total_incidents": total,
        "incidents_last_24h": recent,
        "risk_distribution": risk_counts
    }), 200

# -------------------------
# Failed Login Activity Route
# -------------------------
@app.route("/failed-logins", methods=["GET"])
def get_failed_logins():
    username = request.args.get("username")
    minutes = int(request.args.get("minutes", 1440))  # default: last 24h

    cutoff = datetime.utcnow() - timedelta(minutes=minutes)
    query = {
        "event.type": "login",
        "event.status": "failed",
        "timestamp": {"$gte": cutoff}
    }
    if username:
        query["event.username"] = username

    docs = incidents_col.find(query).sort("timestamp", -1)
    results = []

    for d in docs:
        event = d.get("event", {})
        risk = d.get("risk", {})
        action = d.get("action", {})
        detector = d.get("detector", {})

        # Format fields
        user = event.get("username", "unknown")
        risk_level = f"{int(risk.get('score', 0.0) * 100)}%"
        status = "BLOCKED" if action.get("action") == "block_user" else "ALLOWED"

        ip = event.get("ip_address", "unknown")
        country = detector.get("country", "")
        location = f"{ip} ({country})" if country else ip

        reason = "; ".join(detector.get("reasons", [])) or risk.get("explanation", "Failed login")

        ts = d.get("timestamp", datetime.utcnow())
        if isinstance(ts, str):  # if stored as ISO string
            ts = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        time_ago = humanize.naturaltime(datetime.utcnow() - ts)

        results.append({
            "user": user,
            "risk": risk_level,
            "status": status,
            "location": location,
            "reason": reason,
            "time": time_ago
        })

    return jsonify(results), 200
# -------------------------
# File Access Activity 
# Route
@app.route("/file-access", methods=["GET"])
def get_file_access():
    username = request.args.get("username")
    minutes = int(request.args.get("minutes", 1440))  # default last 24h

    cutoff = datetime.utcnow() - timedelta(minutes=minutes)
    query = {"event.type": "file_access", "timestamp": {"$gte": cutoff}}
    if username:
        query["event.username"] = username

    docs = incidents_col.find(query).sort("timestamp", -1)
    results = []

    for d in docs:
        event = d.get("event", {})
        risk = d.get("risk", {})
        action = d.get("action", {})

        # Only include HIGH severity + BLOCKED
        if risk.get("risk", "").lower() != "high":
            continue
        if action.get("action") != "block_user":
            continue

        user = event.get("username", "unknown")

        # Derive action name from access_type
        access_type = event.get("access_type", "read")
        action_name = "Withdrawal" if access_type == "download" else access_type.capitalize()

        severity = risk.get("risk", "low").upper()
        status = "BLOCKED"

        results.append({
            "user": user,
            "action": action_name,
            "severity": severity,
            "status": status
        })

    return jsonify(results), 200


# -------------------------
# Ollama Chat Test Route
# -------------------------
@app.route("/ollama/chat", methods=["POST"])
def ollama_chat():
    body = request.get_json(force=True)
    prompt = body.get("prompt", "")
    model = body.get("model", "mistral:7b")

    resp = ollama_generate(prompt, model=model)
    return jsonify({"response": resp}), 200

# -------------------------
# Run server
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
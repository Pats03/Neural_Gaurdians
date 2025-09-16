from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

import redis


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["neuralguardians"]


# Collections
incidents_col = db["incidents"]
users_col = db["users"]   # ✅ used for blocking users
# login_events_col = db["login_attempts"]
users=db["newusers"]  # ✅ used for registration and login
suspicious_domains_col = db["suspicious_domains"]
admins_col = db["admins"]
file_access_col = db["file_access_logs"]
# # detectors/login_detector.py
# from typing import Dict

# def detect_abnormal_login(event: Dict) -> Dict:
#     failed = int(event.get("failed_logins", 0))
#     ip_country = str(event.get("ip_country", "")).upper()
#     hour = event.get("hour_of_day", None)
#     reasons = []

#     if failed >= 5:
#         reasons.append(f"High failed login attempts: {failed}")

#     suspicious_countries = {"RU", "CN", "KP", "IR"}
#     if ip_country and ip_country in suspicious_countries:
#         reasons.append(f"Login from suspicious country: {ip_country}")

#     if hour is not None and (hour < 6 or hour > 23):
#         reasons.append(f"Unusual login hour: {hour}")

#     score = min(1.0, 0.2 * failed + (0.5 if ip_country in suspicious_countries else 0) + (0.2 if hour and (hour < 6 or hour > 23) else 0))
#     return {"alert": len(reasons) > 0, "reasons": reasons, "score": score}
# from typing import Dict

# from datetime import datetime

# def get_country_from_ip(ip: str) -> str:
#     # In a real system, you'd use a service like MaxMind GeoLite2.
#     if ip.startswith("192.0.2."):
#         return "US"
#     if ip.startswith("203.0.113."):
#         return "CN"
#     if ip.startswith("198.51.100."):
#         return "RU"
#     return "UNKNOWN"
# RISKY_COUNTRIES = ["RU", "CN", "KP", "IR"]

# def detect_abnormal_login(event: Dict) -> Dict:
#     reasons, score, alert = [], 0.0, False

#     ip = event.get("ip_address", "unknown")
#     country = event.get("ip_country") or get_country_from_ip(ip)

#     if event.get("failed_logins", 0) > 5:
#         reasons.append("Multiple failed login attempts")
#         score += 0.5

#     hour = event.get("hour_of_day", datetime.utcnow().hour)
#     if hour < 6 or hour > 23:
#         reasons.append(f"Login attempt at unusual hour: {hour}")
#         score += 0.2

#     if country in RISKY_COUNTRIES:
#         reasons.append(f"Login from high-risk country: {country}")
#         score += 0.3

#     if score >= 0.5:
#         alert = True

#     return {
#         "alert": alert,
#         "reasons": reasons,
#         "score": round(score, 2),
#         "ip": ip,
#         "country": country
#     }

# from typing import Dict
# from datetime import datetime, timedelta
# from db import users_col, login_attempts_col
# from geoip_client import get_country_for_ip

# FAILED_LOGIN_LIMIT = 5
# RESET_WINDOW_MINUTES = 15

# RISKY_COUNTRIES = ["RU", "CN", "KP", "IR"]

# def detect_abnormal_login(event: Dict) -> Dict:
#     reasons, score, alert = [], 0.0, False

#     ip = event.get("ip_address", "unknown")
#     username = event.get("username", "unknown")
#     country = get_country_for_ip(ip)

#     failed = int(event.get("failed_logins", 0))
#     if failed > 0:
#         cutoff = datetime.utcnow() - timedelta(minutes=RESET_WINDOW_MINUTES)
#         login_attempts_col.delete_many({"username": username, "timestamp": {"$lt": cutoff}})
#         for _ in range(failed):
#             login_attempts_col.insert_one({"username": username, "timestamp": datetime.utcnow()})

#     failed_count = login_attempts_col.count_documents({"username": username})

#     if failed_count > FAILED_LOGIN_LIMIT:
#         reasons.append(f"Too many failed login attempts ({failed_count})")
#         score += 0.6
#         users_col.update_one({"username": username}, {"$set": {"status": "blocked"}}, upsert=True)

#     hour = event.get("hour_of_day", datetime.utcnow().hour)
#     if hour < 6 or hour > 23:
#         reasons.append(f"Login attempt at unusual hour: {hour}")
#         score += 0.2

#     if country in RISKY_COUNTRIES:
#         reasons.append(f"Login from high-risk country: {country} (IP: {ip})")
#         score += 0.3

#     if score >= 0.5:
#         alert = True

#     return {
#         "alert": alert,
#         "reasons": reasons,
#         "score": round(score, 2),
#         "ip": ip,
#         "country": country,
#         "failed_logins": failed_count
#     }


# from typing import Dict
# from datetime import datetime, timedelta, timezone
# from db import users_col, login_events_col
# from geoip_client import get_country_for_ip

# FAILED_LOGIN_LIMIT = 5
# RESET_WINDOW_MINUTES = 15
# RISKY_COUNTRIES = ["RU", "CN", "KP", "IR"]


# def detect_abnormal_login(event: Dict) -> Dict:
#     reasons, score, alert = [], 0.0, False

#     username = event.get("username", "unknown")
#     ip = event.get("ip_address", "unknown")
#     country = event.get("ip_country") or get_country_for_ip(ip)

#     # 1. Cleanup old login attempts (older than RESET_WINDOW_MINUTES)
#     cutoff = datetime.now(timezone.utc) - timedelta(minutes=RESET_WINDOW_MINUTES)
#     login_events_col.delete_many({"username": username, "timestamp": {"$lt": cutoff}})

#     # 2. Count total attempts (failed only for risk calc, but we still log all)
#     total_attempts = login_events_col.count_documents({"username": username})

#     # 3. Add this new attempt
#     attempt_number = total_attempts + 1
#     event["attempt_number"] = attempt_number  # enrich event
#     login_events_col.insert_one({
#         "username": username,
#         "status": event.get("status", "unknown"),
#         "ip_address": ip,
#         "ip_country": country,
#         "hour_of_day": event.get("hour_of_day", datetime.now(timezone.utc).hour),
#         "attempt_number": attempt_number,
#         "timestamp": datetime.now(timezone.utc)
#     })

#     # 4. Risk conditions
#     if attempt_number > FAILED_LOGIN_LIMIT and event.get("status") == "failed":
#         reasons.append(f"Too many failed login attempts ({attempt_number})")
#         score += 0.6
#         users_col.update_one({"username": username}, {"$set": {"status": "blocked"}}, upsert=True)

#     hour = event.get("hour_of_day", datetime.now(timezone.utc).hour)
#     if hour < 6 or hour > 23:
#         reasons.append(f"Login attempt at unusual hour: {hour}")
#         score += 0.2

#     if country in RISKY_COUNTRIES:
#         reasons.append(f"Login from high-risk country: {country} (IP: {ip})")
#         score += 0.3

#     if score >= 0.5:
#         alert = True

#     return {
#         "alert": alert,
#         "reasons": reasons,
#         "score": round(score, 2),
#         "ip": ip,
#         "country": country,
#         "attempt_number": attempt_number
#     }


from typing import Dict
from datetime import datetime, timezone
from db import users_col
from geoip_client import get_country_for_ip
import redis
import os

# Config
FAILED_LOGIN_LIMIT = 5
RESET_WINDOW_MINUTES = 15
RISKY_COUNTRIES = ["RU", "CN", "KP", "IR"]

# Redis setup
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def detect_abnormal_login(event: Dict) -> Dict:
    reasons, score, alert = [], 0.0, False

    username = event.get("username", "unknown")
    ip = event.get("ip_address", "unknown")
    country = event.get("ip_country") or get_country_for_ip(ip)

    # ✅ Redis key per user for attempts
    redis_key = f"login_attempts:{username}"

    # 1. Increment attempt counter & set expiry
    attempt_number = r.incr(redis_key)
    r.expire(redis_key, RESET_WINDOW_MINUTES * 60)  # auto reset after window

    # Enrich event with metadata
    event["attempt_number"] = attempt_number
    event["timestamp"] = datetime.now(timezone.utc).isoformat()

    # (Optional) Store details in Redis list for audit
    r.rpush(f"{redis_key}:details", str(event))
    r.expire(f"{redis_key}:details", RESET_WINDOW_MINUTES * 60)

    # 2. Risk conditions
    if attempt_number > FAILED_LOGIN_LIMIT and event.get("status") == "failed":
        reasons.append(f"Too many failed login attempts ({attempt_number})")
        score += 0.6
        users_col.update_one(
            {"username": username},
            {"$set": {"status": "blocked"}},
            upsert=True
        )

    hour = event.get("hour_of_day", datetime.now(timezone.utc).hour)
    if hour < 6 or hour > 23:
        reasons.append(f"Login attempt at unusual hour: {hour}")
        score += 0.2

    if country in RISKY_COUNTRIES:
        reasons.append(f"Login from high-risk country: {country} (IP: {ip})")
        score += 0.3

    if score >= 0.5:
        alert = True

    return {
        "alert": alert,
        "reasons": reasons,
        "score": round(score, 2),
        "ip": ip,
        "country": country,
        "attempt_number": attempt_number
    }




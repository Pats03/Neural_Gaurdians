from typing import Dict
from datetime import datetime, timedelta
from db import file_access_col  # new Mongo collection

# Sensitive rules
SENSITIVE_FILES = [
    "/etc/passwd", "/etc/shadow", "/etc/hosts",
    "/var/log/auth.log", "/var/log/syslog",
    ".env", "config.json", "secrets.json",
]

SENSITIVE_DIRS = [
    "/root", "/home/admin", "/var/lib/mysql", "/var/www/html"
]

# Rule thresholds
SENSITIVE_ACCESS_LIMIT = 3       # in 10 min
BURST_ACCESS_LIMIT = 5           # in 1 min

def detect_file_access(event: Dict) -> Dict:
    username = event.get("username", "unknown")
    filepath = event.get("file_path", "")
    access_type = event.get("access_type", "read")
    ip = event.get("ip_address", "unknown")
    timestamp = datetime.utcnow()

    reasons, score, alert = [], 0.0, False

    # Rule 1: Access to sensitive files
    if any(filepath.endswith(f) for f in SENSITIVE_FILES):
        reasons.append(f"Sensitive file accessed: {filepath}")
        score += 0.7

    # Rule 2: Access to sensitive directories
    if any(filepath.startswith(d) for d in SENSITIVE_DIRS):
        reasons.append(f"Sensitive directory accessed: {filepath}")
        score += 0.6

    # Rule 3: Suspicious extensions
    if filepath.endswith((".db", ".sql", ".pem", ".key")):
        reasons.append(f"Sensitive extension accessed: {filepath}")
        score += 0.5

    # ✅ MongoDB: Store this access event
    file_access_col.insert_one({
        "username": username,
        "file_path": filepath,
        "access_type": access_type,
        "ip": ip,
        "timestamp": timestamp
    })

    # ✅ Rule 4: Excessive sensitive file accesses in 10 min
    cutoff = timestamp - timedelta(minutes=10)
    recent_sensitive = file_access_col.count_documents({
        "username": username,
        "timestamp": {"$gte": cutoff},
        "file_path": {"$in": SENSITIVE_FILES}
    })
    if recent_sensitive > SENSITIVE_ACCESS_LIMIT:
        reasons.append(f"Excessive sensitive file access attempts ({recent_sensitive} in last 10 min)")
        score += 0.8

    # ✅ Rule 5: Burst access detection in 1 min
    burst_cutoff = timestamp - timedelta(minutes=1)
    recent_burst = file_access_col.count_documents({
        "username": username,
        "timestamp": {"$gte": burst_cutoff}
    })
    if recent_burst > BURST_ACCESS_LIMIT:
        reasons.append(f"Suspicious burst activity: {recent_burst} files accessed in under 1 min")
        score += 1.0

    if score >= 0.5:
        alert = True

    return {
        "alert": alert,
        "reasons": reasons,
        "score": round(score, 2),
        "file": filepath,
        "access_type": access_type,
        "user": username,
        "ip": ip,
        "timestamp": timestamp.isoformat()
    }
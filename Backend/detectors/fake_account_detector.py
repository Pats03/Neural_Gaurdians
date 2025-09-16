from typing import Dict
import re
from db import r, users_col, suspicious_domains_col
from datetime import datetime

# Mongo collection for storing flagged domains


# Seed list (initial known bad domains)
SEED_DOMAINS = [
    "tempmail.com", "10minutemail.com", "mailinator.com",
    "yopmail.com", "guerrillamail.com"
]

def is_domain_suspicious(domain: str) -> bool:
    # check against seed list
    if domain in SEED_DOMAINS:
        return True
    # check against DB-learned suspicious domains
    return suspicious_domains_col.find_one({"domain": domain}) is not None

def learn_suspicious_domain(domain: str, reason: str):
    suspicious_domains_col.update_one(
        {"domain": domain},
        {"$set": {"domain": domain, "reason": reason, "flagged_at": datetime.utcnow()}},
        upsert=True
    )

def detect_fake_account(event: Dict) -> Dict:
    username = event.get("username", "unknown")
    email = event.get("email", "")
    ip = event.get("ip_address", "unknown")

    reasons, score, alert = [], 0.0, False
    domain = email.split("@")[-1] if "@" in email else ""

    # 1. Username anomalies
    if len(username) < 4:
        reasons.append("Suspiciously short username")
        score += 0.3
    if re.match(r"^[a-z]*[0-9]{3,}$", username):  # auto-gen pattern
        reasons.append("Username looks auto-generated")
        score += 0.4
    if len(set(username)) <= 2:
        reasons.append("Username has low character diversity")
        score += 0.3

    # 2. Email anomalies
    if domain:
        if is_domain_suspicious(domain):
            reasons.append(f"Suspicious email domain used: {domain}")
            score += 0.5
        if re.match(r"^[a-z]{3,}\d{3,}@.*", email):
            reasons.append("Email looks machine-generated")
            score += 0.3

    # 3. Multiple accounts from same IP
    if ip and ip != "unknown":
        key = f"account_creations:{ip}"
        count = r.incr(key)
        r.expire(key, 120)  # track within 2 mins
        if count > 3:
            reasons.append(f"Multiple accounts created from same IP ({count} in 2mins)")
            score += 0.6

    # Final decision
    if score >= 0.5:
        alert = True
        # ✅ learn from this incident: add domain if it wasn’t in seed list
        if domain and not is_domain_suspicious(domain):
            learn_suspicious_domain(domain, "Flagged via fake account detection")

    return {
        "alert": alert,
        "reasons": reasons,
        "score": round(score, 2),
        "ip": ip,
        "username": username,
        "email": email,
        "domain": domain
    }
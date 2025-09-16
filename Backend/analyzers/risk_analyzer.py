from typing import Dict
from db import suspicious_domains_col 
from datetime import datetime, timedelta

# collection for adaptive learning

def analyze_risk(detector_output: Dict) -> Dict:
    score = detector_output.get("score", 0.0)
    reasons = detector_output.get("reasons", [])
    alert = detector_output.get("alert", False)

    if not alert:
        return {
            "risk": "low",
            "score": round(score, 2),
            "explanation": "No suspicious signals detected"
        }

    # Rule: High risk if score >= 0.8 or explicit high-risk reason
    if score >= 0.8 or any("high-risk" in r.lower() for r in reasons):
        return {
            "risk": "high",
            "score": round(score, 2),
            "explanation": "; ".join(reasons)
        }

    # Rule: Medium risk if score >= 0.4
    risk = "medium" if score >= 0.4 else "low"
    explanation = "; ".join(reasons)

    # ✅ Adaptive escalation: check new suspicious domains in the last hour
    last_hour = datetime.utcnow() - timedelta(hours=1)
    recent_suspicious_domains = suspicious_domains_col.count_documents({
        "flagged_at": {"$gte": last_hour}
    })

    if recent_suspicious_domains >= 5 and risk != "high":
        risk = "high"
        explanation += f" | Escalated: {recent_suspicious_domains} new suspicious domains flagged in the last hour"

    return {
        "risk": risk,
        "score": round(score, 2),
        "explanation": explanation
    }
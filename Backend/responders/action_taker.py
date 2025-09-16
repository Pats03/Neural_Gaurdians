# # responders/action_taker.py
# from typing import Dict

# def take_action(risk: Dict, event: Dict) -> Dict:
#     level = risk.get("risk", "low")
#     user = event.get("username", "unknown")

#     if level == "high":
#         return {"action": "block_user", "details": {"user": user, "reason": risk.get("explanation")}}
#     elif level == "medium":
#         return {"action": "reset_session", "details": {"user": user, "reason": risk.get("explanation")}}
#     else:
#         return {"action": "allow", "details": {"user": user, "note": "no action"}}

from typing import Dict
from db import users_col


def block_user_in_db(username: str):
    users_col.update_one({"username": username}, {"$set": {"status": "blocked"}}, upsert=True)

def reset_user_session(username: str):
    users_col.update_one({"username": username}, {"$set": {"session_reset": True}}, upsert=True)

def take_action(risk: Dict, event: Dict) -> Dict:
    user = event.get("username", "unknown")
    level = risk.get("risk", "low")

    if level == "high":
        block_user_in_db(user)
        return {"action": "block_user", "details": {"user": user, "reason": risk.get("explanation", ""), "status": "User blocked in DB"}}

    elif level == "medium":
        reset_user_session(user)
        return {"action": "reset_session", "details": {"user": user, "reason": risk.get("explanation", ""), "status": "User session flagged for reset"}}

    return {"action": "allow", "details": {"user": user, "note": "Normal activity"}}

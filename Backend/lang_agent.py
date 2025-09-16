# lang_agent.py
"""
LangGraph workflow (Detector -> Analyzer -> Action)
Persistent memory uses MongoDB (incidents_col from db.py).
Reporter node is skipped for now.
"""

from typing import Dict
from datetime import datetime, timedelta
from langgraph.graph import StateGraph
from db import incidents_col

from detectors.login_detector import detect_abnormal_login
from detectors.file_access_detector import detect_file_access
from detectors.fake_account_detector import detect_fake_account
from analyzers.risk_analyzer import analyze_risk
from responders.action_taker import take_action
from reporters.reporter import generate_report

# ----------------------
# Mongo helpers
# ----------------------
def save_incident(username: str, event: Dict, detector: Dict, risk: Dict, action: Dict,report:str):
    doc = {
        "username": username,
        "type": event.get("type"),
        "timestamp": datetime.utcnow(),
        "event": event,
        "detector": detector,
        "risk": risk,
        "action": action,
        "report":report
    }
    try:
        incidents_col.insert_one(doc)
    except Exception as e:
        print("Error saving incident:", e)


def get_recent_history(username: str, minutes: int = 60):
    cutoff = datetime.utcnow() - timedelta(minutes=minutes)
    try:
        cursor = incidents_col.find({
            "username": username,
            "timestamp": {"$gte": cutoff},
            "risk.risk": {"$in": ["medium", "high"]}
        })
        return list(cursor)
    except Exception as e:
        print("Error querying history:", e)
        return []


# ----------------------
# Node definitions
# ----------------------
def detector_node(state: Dict) -> Dict:
    event = state["event"]
    t = event.get("type", "unknown")

    if t == "login":
        detector_output = detect_abnormal_login(event)
    elif t == "file_access":
        detector_output = detect_file_access(event)
    elif t == "account":
        detector_output = detect_fake_account(event)
    else:
        detector_output = {"alert": False, "reasons": [], "score": 0.0}

    state["detector"] = detector_output
    return state


def analyzer_node(state: Dict) -> Dict:
    event = state["event"]
    username = event.get("username", "unknown")
    detector_output = state["detector"]

    risk = analyze_risk(detector_output)

    # Escalate if user had multiple past suspicious incidents
    history = get_recent_history(username, minutes=60)
    suspicious_count = len(history)

    if suspicious_count >= 3 and risk.get("risk") != "high":
        risk = {
            "risk": "high",
            "score": 0.95,
            "explanation": f"Escalated: {suspicious_count} suspicious incidents in last 60 min"
        }

    state["risk"] = risk
    return state


def action_node(state: Dict) -> Dict:
    risk = state["risk"]
    event = state["event"]

    action = take_action(risk, event)
    state["action"] = action

    # Save final state in DB (since no reporter is present)
  

    return state

def reporter_node(state: Dict) -> Dict:
    event = state["event"]
    detector_output = state["detector"]
    risk = state["risk"]
    action = state["action"]
    username = event.get("username", "unknown")

    report = generate_report(event, detector_output, risk, action, model="llama3")
    save_incident(username, event, detector_output, risk, action, report)

    history = get_recent_history(username, minutes=60)
    if history:
        report += f"\n\n[User History: {len(history)} suspicious incidents in past 60 mins]"

    state["report"] = report
    return state

def safe_reporter_node(state: Dict) -> Dict:
    event = state["event"]
    username = event.get("username", "unknown")
    detector_output = state["detector"]

    risk = {"risk": "low", "score": detector_output.get("score", 0), "explanation": "No suspicious signals"}
    action = {"action": "allow", "details": {"user": username, "note": "normal activity"}}
    report = f"Event {event.get('type')} for user {username} appears normal. No suspicious activity detected."

    save_incident(username, event, detector_output, risk, action, report)

    state["risk"] = risk
    state["action"] = action
    state["report"] = report
    return state
# ----------------------
# Branch function
# ----------------------
def detector_branch(state: Dict) -> str:
    """Decide next step after detector"""
    return "analyzer" if state["detector"].get("alert", False) else "safe_reporter"


# ----------------------
# Build graph
# ----------------------
graph = StateGraph(dict)

graph.add_node("detector", detector_node)
graph.add_node("analyzer", analyzer_node)
graph.add_node("action", action_node)
graph.add_node("reporter", reporter_node)
graph.add_node("safe_reporter", safe_reporter_node)

# Conditional branching: detector -> analyzer OR action
graph.add_conditional_edges(
    "detector",
    detector_branch,
    {
        "analyzer": "analyzer",
        "action": "action",
        "safe_reporter": "safe_reporter",
    }
)

# Linear edge: analyzer -> action

graph.add_edge("analyzer", "action")
graph.add_edge("action", "reporter")
# Entry and finish
graph.set_entry_point("detector")
graph.set_finish_point("reporter")
graph.set_finish_point("safe_reporter")

# Compile into runnable app
app_graph = graph.compile()



# ----------------------
# Run wrapper
# ----------------------
def run_agent(event: Dict) -> Dict:
    state = {"event": event}
    final_state = app_graph.invoke(state)
    return {
        "event": final_state.get("event"),
        "detector": final_state.get("detector"),
        "risk": final_state.get("risk"),
        "action": final_state.get("action"),
        "report": final_state.get("report"),
    }

from typing import Dict
from ollama_client import generate  # ✅ using Ollama locally

def generate_report(event: Dict, detector_output: Dict, risk: Dict, action: Dict, model: str = "llama3") -> str:
    prompt = f"""
    You are a security assistant. Create a clear admin report for this incident.

    Event: {event}
    Detector Findings: {detector_output}
    Risk Analysis: {risk}
    Action Taken: {action}

    Format your response as:
    - User
    - Event Type
    - Risk Level
    - Reasons
    - Action Taken
    - Recommendation (1-2 lines)
    """

    try:
        response = generate(prompt, model=model)
        return response.strip()
    except Exception as e:
        return f"[Error generating report: {e}]"
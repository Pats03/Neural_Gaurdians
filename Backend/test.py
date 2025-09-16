import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"   # your Flask server

def pretty_print(title, resp):
    print(f"\n--- {title} ---")
    try:
        print(json.dumps(resp.json(), indent=2))
    except Exception:
        print("Response:", resp.text)


def test_multiple_ip_logins(username="rum"):
    ips = ["127.0.0.1", "192.168.1.10", "10.0.0.5", "172.16.0.12", "203.0.113.77"]
    
    # simulate multiple failed login attempts from different IPs
    for i, ip in enumerate(ips, start=1):
        event = {
            "type": "login",
            "username": username,
            "ip_address": ip,
            "ip_country": "IN",
            "hour_of_day": 2,
            "status": "failed",
            "failed_logins": 1
        }
        resp = requests.post(f"{BASE_URL}/incident", json=event)
        pretty_print(f"Attempt {i} from {ip}", resp)
        time.sleep(1)  # just to space requests a bit


if __name__ == "__main__":
    test_multiple_ip_logins("rum")
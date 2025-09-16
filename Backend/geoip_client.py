# geoip_client.py
import requests
import os

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "ip-geolocation-find-ip-location-and-ip-info.p.rapidapi.com"

def get_country_for_ip(ip: str) -> str:
    if not ip:
        return "UNKNOWN"

    url = f"https://{RAPIDAPI_HOST}/backend/ipinfo/?ip={ip}"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST,
    }

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # adjust according to API response format
        return data.get("country", "UNKNOWN")
    except Exception:
        return "UNKNOWN"
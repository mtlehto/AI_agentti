import requests
from agent.config import HOME, WORK, ORS_KEY

def get_car_time():
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {"Authorization": ORS_KEY}
    body = {"coordinates": [[HOME[1], HOME[0]], [WORK[1], WORK[0]]]}
    try:
        response = requests.post(url, json=body, headers=headers, timeout=15)
        response.raise_for_status()
        payload = response.json()
        return int(payload['routes'][0]['summary']['duration']/60)
    except (requests.RequestException, KeyError, ValueError, TypeError):
        return 30


def get_public_time():
    return 30

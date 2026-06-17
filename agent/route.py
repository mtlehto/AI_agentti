import requests
from agent.config import HOME, WORK, ORS_KEY

def get_car_time():
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {"Authorization": ORS_KEY}
    body = {"coordinates": [[HOME[1], HOME[0]], [WORK[1], WORK[0]]]}
    r = requests.post(url, json=body, headers=headers).json()
    return int(r['routes'][0]['summary']['duration']/60)


def get_public_time():
    return 30

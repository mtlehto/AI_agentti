import requests
from agent.graph import user_path

def get_calendar(token):
    url = user_path("events?$top=5")
    return [e['subject'] for e in requests.get(url, headers={"Authorization":f"Bearer {token}"}).json().get('value',[])]

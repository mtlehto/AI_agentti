import requests
from agent.graph import user_path

def get_calendar(token):
    url = user_path("events?$top=5")
    try:
        response = requests.get(url, headers={"Authorization":f"Bearer {token}"}, timeout=15)
        response.raise_for_status()
        return [e['subject'] for e in response.json().get('value',[])]
    except requests.RequestException:
        return []

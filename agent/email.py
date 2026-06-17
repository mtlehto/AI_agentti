import requests
from agent.graph import user_path

def get_emails(token):
    url = user_path("mailFolders/inbox/messages?$top=5")
    try:
        response = requests.get(url, headers={"Authorization":f"Bearer {token}"}, timeout=15)
        response.raise_for_status()
        return [m['subject'] for m in response.json().get('value',[])]
    except requests.RequestException:
        return []

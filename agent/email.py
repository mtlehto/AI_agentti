import requests
from agent.graph import user_path

def get_emails(token):
    url = user_path("mailFolders/inbox/messages?$top=5")
    return [m['subject'] for m in requests.get(url, headers={"Authorization":f"Bearer {token}"}).json().get('value',[])]

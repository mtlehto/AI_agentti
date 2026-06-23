import requests
from agent.config import TEAMS_WEBHOOK_URL


def send(token, text):
    if TEAMS_WEBHOOK_URL:
        try:
            response = requests.post(
                TEAMS_WEBHOOK_URL,
                json={"text": text},
                timeout=15,
            )
            response.raise_for_status()
            return True
        except requests.RequestException:
            return False

    print("Teams send:", text)
    return False

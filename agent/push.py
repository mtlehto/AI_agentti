import requests
from agent.config import PUSHOVER_APP_TOKEN, PUSHOVER_USER_KEY, PUSHOVER_SOUND


def send_push(message, title="Aamubriiffi"):
    if not PUSHOVER_APP_TOKEN or not PUSHOVER_USER_KEY:
        return False

    payload = {
        "token": PUSHOVER_APP_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "title": title,
        "message": message,
    }
    if PUSHOVER_SOUND:
        payload["sound"] = PUSHOVER_SOUND

    try:
        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data=payload,
            timeout=15,
        )
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False
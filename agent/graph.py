import msal
from agent.config import *

def get_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )
    t = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return t.get("access_token")


def user_path(resource):
    return f"https://graph.microsoft.com/v1.0/users/{USER_ID}/{resource}"

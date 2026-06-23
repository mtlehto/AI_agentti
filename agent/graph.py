import os
from pathlib import Path
import msal
from agent.config import *


_CACHE_FILE = Path(__file__).parent.parent / ".msal_token_cache"


def _load_cache():
    cache = msal.SerializableTokenCache()
    if _CACHE_FILE.exists():
        try:
            cache.deserialize(_CACHE_FILE.read_bytes())
        except Exception:
            pass
    return cache


def _save_cache(cache):
    try:
        _CACHE_FILE.write_bytes(cache.serialize())
    except Exception:
        pass


def get_token():
    """Return an access token.

    Behavior:
    - If `CLIENT_SECRET` is set, use client credentials (app-only) as before.
    - Otherwise use delegated device-code flow with a persistent local token cache.
    """
    # App-only flow (service principal)
    if CLIENT_SECRET:
        app = msal.ConfidentialClientApplication(
            CLIENT_ID,
            authority=f"https://login.microsoftonline.com/{TENANT_ID}",
            client_credential=CLIENT_SECRET,
        )
        t = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        return t.get("access_token")

    # Delegated flow (user) with device code and cache
    scopes = ["Mail.Read", "Calendars.Read", "Tasks.Read"]
    cache = _load_cache()
    app = msal.PublicClientApplication(CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID or 'common'}", token_cache=cache)

    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(scopes, account=accounts[0])
        if result and "access_token" in result:
            _save_cache(cache)
            return result.get("access_token")

    # Start device code flow
    flow = app.initiate_device_flow(scopes=scopes)
    if "user_code" not in flow:
        return None
    print(flow.get("message"))
    result = app.acquire_token_by_device_flow(flow)
    if result and "access_token" in result:
        _save_cache(cache)
        return result.get("access_token")
    return None


def user_path(resource):
    if USER_ID:
        return f"https://graph.microsoft.com/v1.0/users/{USER_ID}/{resource}"
    return f"https://graph.microsoft.com/v1.0/me/{resource}"

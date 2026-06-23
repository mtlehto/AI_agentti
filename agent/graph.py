import os
from pathlib import Path
import msal
from agent.config import *


_CACHE_FILE = Path(__file__).parent.parent / ".msal_token_cache"


def _load_cache():
    cache = msal.SerializableTokenCache()
    if _CACHE_FILE.exists():
        try:
            data = _CACHE_FILE.read_bytes()
            if data:
                cache.deserialize(data)
        except Exception as e:
            print("Warning: failed to load MSAL cache:", e)
    return cache


def _save_cache(cache):
    try:
        data = cache.serialize()
        # atomic write
        tmp = _CACHE_FILE.with_suffix(".tmp")
        tmp.write_bytes(data)
        tmp.replace(_CACHE_FILE)
    except Exception as e:
        print("Warning: failed to save MSAL cache:", e)


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
    scopes = ["Mail.Read", "Calendars.Read", "Tasks.Read", "offline_access"]
    cache = _load_cache()
    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID or 'common'}",
        token_cache=cache,
    )

    # Try silent acquisition first (uses refresh token if available)
    accounts = app.get_accounts()
    if accounts:
        try:
            result = app.acquire_token_silent(scopes, account=accounts[0])
            if result and "access_token" in result:
                _save_cache(cache)
                return result.get("access_token")
        except Exception as e:
            print("Info: acquire_token_silent failed:", e)

    # Start device code flow if silent failed
    try:
        flow = app.initiate_device_flow(scopes=scopes)
    except Exception as e:
        print("Error initiating device flow:", e)
        return None

    if "user_code" not in flow:
        return None
    print(flow.get("message"))
    try:
        result = app.acquire_token_by_device_flow(flow)
    except Exception as e:
        print("Error during device flow:", e)
        return None

    if result and "access_token" in result:
        _save_cache(cache)
        return result.get("access_token")
    return None


def user_path(resource):
    if USER_ID:
        return f"https://graph.microsoft.com/v1.0/users/{USER_ID}/{resource}"
    return f"https://graph.microsoft.com/v1.0/me/{resource}"

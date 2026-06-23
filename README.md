# AI agentti

Python-projekti, joka kokoaa Outlookin, kalenterin, tehtävät ja liikennetiedot aamubriiffiksi.

Paikallisesti isännöity FastAPI-palvelu, joka toimii Windows/Mac/Linux-koneella.

## Vaatimukset

- Python 3.11 tai Docker
- Microsoft Graph API -oikeudet (TENANT_ID, CLIENT_ID, CLIENT_SECRET, USER_ID)
- Oleellinen: Ollama asennettuna paikallisesti AI-päättelyä varten

## Asennus ja käynnistys

### 1. Perustiedot

Kopioi ympäristömuuttujat:

```powershell
Copy-Item .env.example .env
```

Täytä `.env`-tiedostoon seuraavat arvot:

- `TENANT_ID` — Microsoft Entra ID tenant ID
- `CLIENT_ID` — Entra ID app registration client ID
- `CLIENT_SECRET` — App registration secret
- `USER_ID` — Microsoft Graph user ID
- `ORS_KEY` — OpenRouteService API key (reititykselle)
- `PUSHOVER_APP_TOKEN` — (valinnainen) Pushover app token
- `PUSHOVER_USER_KEY` — (valinnainen) Pushover user key
- `TEAMS_WEBHOOK_URL` — (valinnainen) Teams webhook URL

### 2. Paikallinen käyttö (Python)

```powershell
# Asenna riippuvuudet
pip install -r requirements.txt

# Käynnistä API
uvicorn agent.api:app --host 0.0.0.0 --port 8000
```

Avaa selaimeen `http://localhost:8000/brief` tai `http://localhost:8000/morning`.

### 3. Paikallinen käyttö (Docker)

```powershell
# Käynnistä Dockerissa
docker compose up --build

# Avaa http://localhost:8000
```

Tulostettu aamubriiffi tallennetaan `./output/aamubriiffi.mp3`.

## Käyttö iPhonesta

### Apple Shortcuts

1. Luo Shortcuts-automaatio, joka käynnistyy kun hälytys sammuu tai tiettyyn aikaan aamulla.
2. Lisää toiminto `Get Contents of URL` ja osoita se polkuun `http://<YOUR_LOCAL_IP>:8000/brief?persona=arska`.
3. Lisää toiminto `Show Result` tai `Speak Text`, jotta saat briiffin puhelimeen.
4. Luo erillinen Siri-shortcut, joka kutsuu samaa URL:ia.

### Push-ilmoitukset

Jos haluat oikean push-ilmoituksen iPhoneen:

1. Asenna Pushover iPhoneen.
2. Luo Pushover-sovellus ja kopioi App Token.
3. Kopioi henkilökohtainen User Key.
4. Lisää arvot `.env`-tiedostoon muuttujina `PUSHOVER_APP_TOKEN` ja `PUSHOVER_USER_KEY`.

## Huomio

Projektin Microsoft Graph -kutsut käyttävät app tokenia ja `USER_ID`-polkua, joten sovellusvaatimuksissa pitää olla sopivat Graph-oikeudet.

AI-päätelmä tapahtuu `ollama`-runtimessa, joka pitää asentaa paikallisesti:

```powershell
# https://ollama.ai — lataa ja asenna
ollama run mistral
```

## Personal accounts (delegated auth)

If you use personal Microsoft accounts (MSA) for email, calendar or tasks, the app must use delegated authentication (user consent). App-only (client credential) tokens cannot access personal MSA mailboxes.

Quick steps to enable local delegated sign-in:

- In Azure portal, register an app and set "Supported account types" to include personal Microsoft accounts ("Accounts in any organizational directory and personal Microsoft accounts").
- In the app's Authentication settings enable "Mobile and desktop applications" if you plan to use device code.
- Add delegated API permissions: `Mail.Read`, `Calendars.Read`, `Tasks.Read`, and `offline_access` and grant consent as appropriate.

Device code (local) example — add to `agent/graph.py` or a new `agent/auth.py`:

```python
import os
import msal

CLIENT_ID = os.getenv("CLIENT_ID")
TENANT = os.getenv("TENANT_ID") or "common"
SCOPES = ["Mail.Read", "Calendars.Read", "Tasks.Read", "offline_access"]

def get_delegated_token():
	app = msal.PublicClientApplication(CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT}")
	flow = app.initiate_device_flow(scopes=SCOPES)
	if "user_code" not in flow:
		raise ValueError("Failed to create device flow")
	print(flow["message"])  # instructs the user to open the URL and enter the code
	result = app.acquire_token_by_device_flow(flow)  # blocks until auth completed or times out
	return result.get("access_token")
```

Recommended code changes:

- In `agent/graph.py` use delegated flow when `CLIENT_SECRET` is not set (no app credentials). Use `get_delegated_token()` to acquire tokens interactively for local runs.
- Prefer the `me` endpoints for delegated accounts (example):

```python
def user_path(resource):
	if USER_ID:
		return f"https://graph.microsoft.com/v1.0/users/{USER_ID}/{resource}"
	return f"https://graph.microsoft.com/v1.0/me/{resource}"
```

Persist the MSAL token cache to a local file so device flow doesn't prompt every run. For production or multi-user deployments, use proper delegated consent flows or service principals as appropriate.


## (Valinnainen) Azure-käyttöönotto

Jos haluat siirtää palvelun pilveen, katso `azure-pipelines.yml` ja `docker-compose.azure.yml`. Nämä vaativat maksullisen Azure-tilauksen.

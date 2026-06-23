import os
from dotenv import load_dotenv
load_dotenv()
TENANT_ID=os.getenv("TENANT_ID")
CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")
USER_ID=os.getenv("USER_ID")
ORS_KEY=os.getenv("ORS_KEY")
PUSHOVER_APP_TOKEN=os.getenv("PUSHOVER_APP_TOKEN")
PUSHOVER_USER_KEY=os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_SOUND=os.getenv("PUSHOVER_SOUND")
TEAMS_WEBHOOK_URL=os.getenv("TEAMS_WEBHOOK_URL")


def _float_env(name, default):
	value = os.getenv(name)
	if value in (None, ""):
		return default
	try:
		return float(value)
	except ValueError:
		return default


HOME = (_float_env("HOME_LAT", 60.20), _float_env("HOME_LON", 24.65))
WORK = (_float_env("WORK_LAT", 60.17), _float_env("WORK_LON", 24.94))

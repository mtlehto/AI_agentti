import os
from dotenv import load_dotenv
load_dotenv()
TENANT_ID=os.getenv("TENANT_ID")
CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")
USER_ID=os.getenv("USER_ID")
ORS_KEY=os.getenv("ORS_KEY")
HOME=(float(os.getenv("HOME_LAT")),float(os.getenv("HOME_LON")))
WORK=(float(os.getenv("WORK_LAT")),float(os.getenv("WORK_LON")))

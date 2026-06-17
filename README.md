# Ultimate Agent Enterprise

Python-projekti, joka kokoaa Outlookin, kalenterin, tehtävät ja liikennetiedot aamubriiffiksi.

## Käyttö

1. Kopioi ympäristömuuttujat tiedostosta `.env.template` tiedostoon `.env`.
2. Asenna riippuvuudet `pip install -r requirements.txt`.
3. Käynnistä API komennolla `uvicorn agent.api:app --host 0.0.0.0 --port 8000`.

## Huomio

Projektin Microsoft Graph -kutsut käyttävät app tokenia ja `USER_ID`-polkua, joten sovellusvaatimuksissa pitää olla sopivat Graph-oikeudet.
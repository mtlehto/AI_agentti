# AI agentti

Python-projekti, joka kokoaa Outlookin, kalenterin, tehtävät ja liikennetiedot aamubriiffiksi.

## Käyttö

1. Kopioi ympäristömuuttujat tiedostosta `.env.example` tiedostoon `.env`.
2. Asenna riippuvuudet `pip install -r requirements.txt`.
3. Käynnistä API komennolla `uvicorn agent.api:app --host 0.0.0.0 --port 8000`.

## iPhone ja Siri

Paras tapa käyttää tätä iPhonessa on Apple Shortcuts:

1. Tee Shortcuts-automaatio, joka käynnistyy kun hälytys sammuu tai tiettyyn aikaan aamulla.
2. Lisää toiminto `Get Contents of URL` ja osoita se polkuun `/brief?persona=arska`.
3. Lisää toiminto `Show Result` tai `Speak Text`, jotta saat briiffin puhelimeen.
4. Tee erillinen Siri-shortcut, joka kutsuu samaa URL:ia, jolloin voit sanoa esimerkiksi “Hei Siri, aamubriiffi”.

Jos haluat varsinaisen push-ilmoituksen ilman Shortcutsia, tarvitaan erillinen push-kanava kuten Pushover, Telegram tai oma iOS-sovellus.

## Huomio

Projektin Microsoft Graph -kutsut käyttävät app tokenia ja `USER_ID`-polkua, joten sovellusvaatimuksissa pitää olla sopivat Graph-oikeudet.
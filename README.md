# CPH Marathon '25 Billet-overvågningsbot

Denne Flask-applikation er en bot, der overvåger tilgængeligheden af billetter til Copenhagen Marathon 2025 og sender beskeder via Facebook Messenger. For at tilmelde sig servicen skal man skrive til botten på Facebook på følgende side: 
* https://www.facebook.com/profile.php?id=61566582682564

## Lokal opsætning

### Forudsætninger
- Python 3.8+
- pip
- virtualenv (anbefalet)

### Installation
1. Klon repositoriet:
   ``` 
   git clone https://github.com/dit-brugernavn/dit-repo-navn.git
   cd dit-repo-navn
   ```

2. Opret og aktiver et virtuelt miljø:
   ``` 
   python -m venv venv
   source venv/bin/activate  # På Windows: venv\Scripts\activate
   ```

3. Installer afhængigheder:
   ``` 
   pip install -r requirements.txt
   ```

4. Konfigurer miljøvariabler:
   Opret en `.env` fil i rodmappen og tilføj følgende:
   ``` 
   VERIFY_TOKEN=dit_verify_token
   ACCESS_TOKEN=din_facebook_access_token
   ```

5. Kør applikationen:
   ``` 
   flask run
   ```

Applikationen vil nu køre på `http://localhost:5000`.

## Docker

### Byg Docker-image

docker build -t cph-marathon-bot .

### Kør Docker-container

docker run -p 5000:5000 --env-file .env cph-marathon-bot


Applikationen vil nu være tilgængelig på `http://localhost:5000`.

## Heroku-deployment

1. Installer [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

2. Log ind på Heroku:
   ```
   heroku login
   ```

3. Opret en ny Heroku-app:
   ```
   heroku create din-app-navn
   ```

4. Tilføj Heroku remote til dit Git-repository:
   ```
   heroku git:remote -a din-app-navn
   ```

5. Konfigurer miljøvariabler:
   ```
   heroku config:set VERIFY_TOKEN=dit_verify_token
   heroku config:set ACCESS_TOKEN=din_facebook_access_token
   ```

6. Deploy til Heroku:
   ```
   git push heroku main
   ```

7. Åbn appen:
   ```
   heroku open
   ```

8. Se logs:
   ```
   heroku logs --tail
   ```

## Facebook Messenger API-opsætning

1. Gå til [Facebook for Developers](https://developers.facebook.com/) og opret en ny app.

2. Tilføj Messenger-produktet til din app.

3. Under Messenger-indstillinger, generer en Page Access Token for den side, du vil sende beskeder fra.

4. Konfigurer webhooks:
   - Callback URL: `https://din-heroku-app.herokuapp.com/webhook`
   - Verify Token: Det samme som dit `VERIFY_TOKEN` i miljøvariablerne
   - Vælg de nødvendige subscriptions (f.eks. messages, messaging_postbacks)

5. Abonner din side på app-events.

6. Opdater din `.env` fil og Heroku config vars med den genererede access og verify-token.

Husk at holde dine tokens og andre følsomme oplysninger hemmelige og aldrig dele dem offentligt eller inkludere dem i dit versionsstyrede kode.

Dette README-dokument giver en grundlæggende oversigt over, hvordan man sætter projektet op lokalt, med Docker, på Heroku, og hvordan man konfigurerer Facebook Messenger API. Bemærk, denne readme er autogenereret med clause-3.5-sonnet og er ikke gennemtestet om den virker.

TODO: Tilføj addons postgresql database + scheduling på heroku.
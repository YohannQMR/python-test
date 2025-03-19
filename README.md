# Python API Test

Une simple API Python utilisant Flask avec un endpoint `/ping` qui répond "pong".

## Installation

1. Clonez ce dépôt
2. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```

## Utilisation

1. Lancez l'application :
   ```
   python app.py
   ```

2. L'API démarre sur `http://localhost:5000`

3. Testez l'endpoint `/ping` :
   ```
   curl http://localhost:5000/ping
   ```
   
   Réponse attendue :
   ```json
   {
     "message": "pong"
   }
   ```

## Endpoints disponibles

- `GET /` : Page d'accueil
- `GET /ping` : Répond avec un message "pong"

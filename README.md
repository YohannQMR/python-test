# Python API Test

Une API REST Python complète utilisant Flask avec authentification JWT et gestion de tâches.

## Fonctionnalités

- Endpoint `/ping` basique qui répond "pong"
- Documentation API complète via Swagger UI
- Authentification utilisateur avec JWT
  - Inscription et connexion
  - Rafraîchissement des tokens
  - Protection des routes
- API CRUD complète pour la gestion de tâches
  - Création, lecture, mise à jour et suppression
  - Filtrage et pagination
  - Basculement de l'état des tâches
- Tests unitaires avec pytest
- Intégration continue via GitHub Actions
- Validation de données avec Marshmallow
- Journalisation (logging)

## Installation

1. Clonez ce dépôt
   ```
   git clone https://github.com/YohannQMR/python-test.git
   cd python-test
   ```

2. Créez et activez un environnement virtuel
   ```
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. Installez les dépendances
   ```
   pip install -r requirements.txt
   ```

4. Configurez les variables d'environnement
   ```
   cp .env.example .env
   # Modifiez les valeurs dans .env selon vos besoins
   ```

## Utilisation

1. Lancez l'application
   ```
   python app.py
   ```

2. L'API démarre sur `http://localhost:5000`

3. Explorez la documentation API
   ```
   http://localhost:5000/api/docs
   ```

## Endpoints disponibles

### Base
- `GET /` : Page d'accueil
- `GET /ping` : Répond avec un message "pong"
- `GET /api/docs` : Documentation Swagger UI

### Authentification
- `POST /auth/register` : Inscription d'un nouvel utilisateur
- `POST /auth/login` : Connexion d'un utilisateur existant
- `GET /auth/me` : Récupérer les informations de l'utilisateur connecté
- `POST /auth/refresh` : Rafraîchir le token d'accès

### Gestion des tâches
- `GET /api/tasks` : Liste des tâches (avec pagination et filtrage)
- `POST /api/tasks` : Créer une nouvelle tâche
- `GET /api/tasks/{id}` : Détails d'une tâche spécifique
- `PUT /api/tasks/{id}` : Mettre à jour une tâche
- `DELETE /api/tasks/{id}` : Supprimer une tâche
- `PATCH /api/tasks/{id}/toggle` : Basculer l'état de complétion d'une tâche

## Tests

Exécuter les tests avec pytest :
```
pytest
```

## Roadmap

Consultez [ROADMAP.md](ROADMAP.md) pour les fonctionnalités prévues.

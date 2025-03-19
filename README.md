# Python API Test

Une API REST Python complète utilisant Flask avec authentification JWT, gestion de tâches et configuration prête pour la production.

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
- Système de limitation de débit (Rate Limiting)
- Monitoring avec Prometheus et Grafana
- Tests de charge avec Locust
- Conteneurisation avec Docker et Docker Compose
- Système de configuration centralisé pour différents environnements
- Base de données relationnelle (SQLite en développement, PostgreSQL en production)

## Installation

### Méthode standard

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

5. Lancez l'application
   ```
   python app.py
   ```

### Avec Docker

1. Clonez ce dépôt
   ```
   git clone https://github.com/YohannQMR/python-test.git
   cd python-test
   ```

2. Démarrez les conteneurs avec Docker Compose
   ```
   docker-compose up -d
   ```

3. L'API est accessible à `http://localhost:5000`
4. Prometheus à `http://localhost:9090`
5. Grafana à `http://localhost:3000` (admin/admin par défaut)

## Endpoints disponibles

### Base
- `GET /` : Page d'accueil
- `GET /ping` : Répond avec un message "pong"
- `GET /health` : Vérifie l'état de santé de l'API
- `GET /api/docs` : Documentation Swagger UI
- `GET /metrics` : Métriques Prometheus (pour le monitoring)

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

### Tests unitaires

Exécuter les tests avec pytest :
```
pytest
```

### Tests de charge

Voir [LOAD_TESTING.md](LOAD_TESTING.md) pour les instructions détaillées sur l'utilisation de Locust pour les tests de charge.

## Monitoring

L'application est configurée avec Prometheus pour collecter des métriques et Grafana pour les visualiser.

1. Accédez à Prometheus : `http://localhost:9090`
2. Accédez à Grafana : `http://localhost:3000` (admin/admin)

## Roadmap

Consultez [ROADMAP.md](ROADMAP.md) pour les fonctionnalités prévues.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

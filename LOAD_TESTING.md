# Tests de charge avec Locust

Ce document explique comment utiliser Locust pour tester les performances de l'API.

## À propos de Locust

Locust est un outil de test de charge open-source, facile à utiliser et programmable en Python. Il permet de simuler des milliers d'utilisateurs simultanés accédant à votre application.

## Installation

Locust est déjà inclus dans les dépendances du projet. Si vous n'avez pas encore installé les dépendances :

```bash
pip install -r requirements.txt
```

## Exécution des tests de charge

1. Assurez-vous que votre API est en cours d'exécution :

```bash
python app.py
```

2. Dans un terminal séparé, démarrez Locust :

```bash
locust -f locustfile.py
```

3. Ouvrez votre navigateur à l'adresse http://localhost:8089

4. Dans l'interface web de Locust, configurez votre test :
   - Number of users : Nombre d'utilisateurs virtuels à simuler
   - Spawn rate : Taux de création des utilisateurs par seconde
   - Host : URL de votre API (par exemple : http://localhost:5000)

5. Cliquez sur "Start swarming" pour démarrer le test

## Interprétation des résultats

L'interface web de Locust affiche les statistiques en temps réel :

- **Request statistics** : Métriques de performance pour chaque endpoint
  - Requests per second (RPS)
  - Temps de réponse moyen
  - Taux d'échec
  
- **Response Time (ms)** : Graphique des temps de réponse au fil du temps

- **Total Requests per Second** : Graphique du nombre de requêtes par seconde

- **Number of Users** : Graphique du nombre d'utilisateurs virtuels actifs

## Scénarios de test implémentés

Notre fichier `locustfile.py` simule un utilisateur réel qui :

1. S'enregistre ou se connecte à l'API
2. Accède à diverses pages comme l'accueil et la vérification de santé
3. Crée, récupère, met à jour et supprime des tâches
4. Rafraîchit son token d'authentification
5. Accède à la documentation API

Les différentes actions ont des poids différents pour simuler un usage réaliste de l'API.

## Personnalisation des tests

Pour personnaliser les tests, vous pouvez modifier le fichier `locustfile.py` :

- Ajuster les poids des tâches (la fréquence relative de chaque action)
- Ajouter de nouvelles actions ou endpoints à tester
- Modifier les temps d'attente entre les actions

## Exécution en mode headless (sans interface graphique)

Pour les environnements CI/CD ou les serveurs sans interface graphique :

```bash
locust -f locustfile.py --headless -u 100 -r 10 -t 5m --host=http://localhost:5000
```

Où :
- `-u 100` : 100 utilisateurs
- `-r 10` : Taux de création de 10 utilisateurs par seconde
- `-t 5m` : Durée du test de 5 minutes
- `--host` : URL de l'API

## Exportation des résultats

Vous pouvez exporter les résultats dans différents formats (CSV, HTML) depuis l'interface web ou en utilisant les options en ligne de commande avec le mode headless.

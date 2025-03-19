FROM python:3.9-slim

WORKDIR /app

# Copier les fichiers de dépendances et installer les packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application
COPY . .

# Exposer le port sur lequel l'application s'exécute
EXPOSE 5000

# Créer un utilisateur non-root pour exécuter l'application
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Commande pour démarrer l'application
CMD ["python", "app.py"]

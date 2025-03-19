import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class Config:
    """Configuration de base pour l'application."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 heure
    JWT_REFRESH_TOKEN_EXPIRES = 2592000  # 30 jours
    
    # Configuration Limiter
    RATELIMIT_DEFAULT = "100 per day, 10 per hour, 1 per second"
    RATELIMIT_STORAGE_URL = "memory://"
    RATELIMIT_STRATEGY = "fixed-window"
    RATELIMIT_HEADERS_ENABLED = True
    
    # Configuration de logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

class DevelopmentConfig(Config):
    """Configuration pour le développement."""
    DEBUG = True
    
class TestingConfig(Config):
    """Configuration pour les tests."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
class ProductionConfig(Config):
    """Configuration pour la production."""
    DEBUG = False
    RATELIMIT_DEFAULT = "1000 per day, 100 per hour, 5 per second"
    # En production, utiliser Redis pour le stockage des compteurs de limitation
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'memory://')

# Dictionnaire des configurations disponibles
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Obtenir la configuration basée sur l'environnement."""
    env = os.getenv('FLASK_ENV', 'default')
    return config.get(env, config['default'])

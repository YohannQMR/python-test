from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_flask_exporter import PrometheusMetrics
import logging
import os
import json
from config import get_config
from models import db, User, Task
from auth import auth_bp
from tasks import tasks_bp

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("api.log")
    ]
)
logger = logging.getLogger(__name__)

# Création et configuration de l'application Flask
app = Flask(__name__)
app.config.from_object(get_config())

# Initialisation des extensions
db.init_app(app)
jwt = JWTManager(app)
CORS(app)

# Configuration du rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day", "10 per hour", "1 per second"],
    strategy="fixed-window"
)

# Configuration Prometheus metrics
metrics = PrometheusMetrics(app)
metrics.info('api_info', 'API Info', version='1.0.0')

# Métriques par défaut
metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)

# Métriques personnalisées
endpoint_counter = metrics.counter(
    'endpoint_counter', 'Endpoint request counter',
    labels={'endpoint': lambda: request.endpoint}
)

# Configuration Swagger
SWAGGER_URL = '/api/docs'
API_URL = '/api/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Python API Test"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Enregistrement des blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(tasks_bp)

@app.route('/api/swagger.json')
def swagger_json():
    with open('swagger.json') as f:
        return jsonify(json.load(f))

# Endpoint /ping qui répond avec "pong" (pas besoin d'authentification)
@app.route('/ping', methods=['GET'])
@limiter.exempt  # Exemption de limite pour cet endpoint
@endpoint_counter
def ping():
    """
    Endpoint simple qui répond 'pong'
    ---
    responses:
      200:
        description: Retourne un message pong
    """
    logger.info("Endpoint /ping appelé")
    return jsonify({"message": "pong"})

# Route par défaut
@app.route('/', methods=['GET'])
@limiter.exempt  # Exemption de limite pour cet endpoint
@endpoint_counter
def home():
    """
    Page d'accueil de l'API
    ---
    responses:
      200:
        description: Liste les endpoints disponibles
    """
    logger.info("Endpoint / appelé")
    return jsonify({
        "message": "Bienvenue sur l'API de test", 
        "endpoints": [
            "/ping", 
            "/api/docs",
            "/auth/register",
            "/auth/login",
            "/auth/refresh",
            "/auth/me",
            "/api/tasks",
            "/metrics",
            "/health"
        ]
    })

# Route de statut/santé de l'API
@app.route('/health', methods=['GET'])
@limiter.exempt  # Exemption de limite pour cet endpoint
def health():
    """
    Endpoint de vérification de santé de l'API
    ---
    responses:
      200:
        description: API en fonctionnement normal
      500:
        description: Problème avec l'API
    """
    try:
        # Vérifier la connexion à la base de données
        db_ok = False
        with app.app_context():
            db.session.execute("SELECT 1").scalar()
            db_ok = True

        status = {
            "status": "ok",
            "database": "connected" if db_ok else "disconnected",
            "api_version": "1.0.0"
        }
        
        if not db_ok:
            return jsonify(status), 500
            
        return jsonify(status)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Health check failed",
            "detail": str(e)
        }), 500

# Gestion des erreurs
@app.errorhandler(404)
def not_found(e):
    logger.warning(f"Erreur 404: {request.path} non trouvé")
    return jsonify({"error": "Route non trouvée"}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Erreur 500: {str(e)}")
    return jsonify({"error": "Erreur serveur interne"}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    logger.warning(f"Rate limit exceeded: {request.remote_addr} - {request.path}")
    return jsonify({
        "error": "Trop de requêtes",
        "message": "Limite de requêtes dépassée. Veuillez réessayer plus tard."
    }), 429

# Création des tables de la base de données
@app.before_first_request
def create_tables():
    db.create_all()
    logger.info("Base de données initialisée")

# Démarrage de l'application si exécuté directement
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import logging
import os
import json
from dotenv import load_dotenv
from models import db, User, Task
from auth import auth_bp
from tasks import tasks_bp

# Charger les variables d'environnement
load_dotenv()

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

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 heure
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 2592000  # 30 jours

# Initialisation des extensions
db.init_app(app)
jwt = JWTManager(app)
CORS(app)

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
            "/api/tasks"
        ]
    })

# Gestion des erreurs
@app.errorhandler(404)
def not_found(e):
    logger.warning(f"Erreur 404: {request.path} non trouvé")
    return jsonify({"error": "Route non trouvée"}), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Erreur 500: {str(e)}")
    return jsonify({"error": "Erreur serveur interne"}), 500

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

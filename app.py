from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
import logging
import os
import json

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

# Création de l'application Flask
app = Flask(__name__)

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

@app.route('/api/swagger.json')
def swagger_json():
    with open('swagger.json') as f:
        return jsonify(json.load(f))

# Endpoint /ping qui répond avec "pong"
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
        "endpoints": ["/ping", "/api/docs"]
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

# Démarrage de l'application si exécuté directement
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

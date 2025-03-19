from flask import Flask, jsonify

# Création de l'application Flask
app = Flask(__name__)

# Endpoint /ping qui répond avec "pong"
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "pong"})

# Route par défaut
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bienvenue sur l'API de test", 
                    "endpoints": ["/ping"]})

# Démarrage de l'application si exécuté directement
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

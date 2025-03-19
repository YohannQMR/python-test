from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from marshmallow import Schema, fields, validate, ValidationError
from models import db, User
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Schéma de validation pour les utilisateurs
class UserSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))

class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

# Enregistrement d'un nouvel utilisateur
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        # Valider les données d'entrée
        schema = UserSchema()
        data = schema.load(request.json)
        
        # Vérifier si l'utilisateur existe déjà
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "Ce nom d'utilisateur est déjà pris"}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Cet email est déjà utilisé"}), 400
        
        # Créer le nouvel utilisateur
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        
        # Ajouter à la base de données
        db.session.add(new_user)
        db.session.commit()
        
        logger.info(f"Nouvel utilisateur créé: {new_user.username}")
        
        # Créer les tokens JWT
        access_token = create_access_token(identity=new_user.id)
        refresh_token = create_refresh_token(identity=new_user.id)
        
        return jsonify({
            "message": "Utilisateur créé avec succès",
            "user": new_user.to_dict(),
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 201
        
    except ValidationError as e:
        logger.warning(f"Validation error during registration: {e.messages}")
        return jsonify({"error": e.messages}), 400
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Une erreur est survenue lors de l'inscription"}), 500

# Connexion d'un utilisateur
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        # Valider les données d'entrée
        schema = LoginSchema()
        data = schema.load(request.json)
        
        # Rechercher l'utilisateur
        user = User.query.filter_by(username=data['username']).first()
        
        # Vérifier l'utilisateur et le mot de passe
        if not user or not user.check_password(data['password']):
            return jsonify({"error": "Nom d'utilisateur ou mot de passe incorrect"}), 401
        
        logger.info(f"Connexion réussie pour: {user.username}")
        
        # Créer les tokens JWT
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            "message": "Connexion réussie",
            "user": user.to_dict(),
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200
        
    except ValidationError as e:
        logger.warning(f"Validation error during login: {e.messages}")
        return jsonify({"error": e.messages}), 400
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return jsonify({"error": "Une erreur est survenue lors de la connexion"}), 500

# Obtenir les informations de l'utilisateur actuel
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    try:
        # Obtenir l'ID de l'utilisateur à partir du token
        user_id = get_jwt_identity()
        
        # Rechercher l'utilisateur dans la base de données
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "Utilisateur non trouvé"}), 404
        
        return jsonify({"user": user.to_dict()}), 200
        
    except Exception as e:
        logger.error(f"Error getting user profile: {str(e)}")
        return jsonify({"error": "Une erreur est survenue"}), 500

# Rafraîchir le token
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        # Obtenir l'ID de l'utilisateur à partir du refresh token
        user_id = get_jwt_identity()
        
        # Générer un nouveau token d'accès
        access_token = create_access_token(identity=user_id)
        
        return jsonify({
            "access_token": access_token
        }), 200
        
    except Exception as e:
        logger.error(f"Error refreshing token: {str(e)}")
        return jsonify({"error": "Une erreur est survenue"}), 500

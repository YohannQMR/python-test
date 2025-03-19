from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, validate, ValidationError
from models import db, Task, User
import logging

logger = logging.getLogger(__name__)

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

# Schéma de validation pour les tâches
class TaskSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=100))
    description = fields.String(required=False)
    completed = fields.Boolean(required=False, default=False)

# Pagination schema
class PaginationSchema(Schema):
    page = fields.Integer(missing=1, validate=validate.Range(min=1))
    per_page = fields.Integer(missing=10, validate=validate.Range(min=1, max=100))

# Obtenir toutes les tâches (avec pagination)
@tasks_bp.route('', methods=['GET'])
@jwt_required()
def get_tasks():
    try:
        # Obtenir l'identité de l'utilisateur actuel
        user_id = get_jwt_identity()
        
        # Valider les paramètres de pagination
        pagination_schema = PaginationSchema()
        params = pagination_schema.load(request.args)
        
        page = params.get('page', 1)
        per_page = params.get('per_page', 10)
        
        # Filtrer par état de complétion si spécifié
        completed = request.args.get('completed')
        query = Task.query.filter_by(user_id=user_id)
        
        if completed is not None:
            completed = completed.lower() == 'true'
            query = query.filter_by(completed=completed)
        
        # Appliquer la pagination
        paginated_tasks = query.order_by(Task.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Préparer la réponse
        response = {
            "tasks": [task.to_dict() for task in paginated_tasks.items],
            "pagination": {
                "total": paginated_tasks.total,
                "pages": paginated_tasks.pages,
                "page": page,
                "per_page": per_page,
                "has_next": paginated_tasks.has_next,
                "has_prev": paginated_tasks.has_prev,
            }
        }
        
        return jsonify(response), 200
        
    except ValidationError as e:
        logger.warning(f"Validation error: {e.messages}")
        return jsonify({"error": e.messages}), 400
    except Exception as e:
        logger.error(f"Error getting tasks: {str(e)}")
        return jsonify({"error": "Une erreur est survenue"}), 500

# Créer une nouvelle tâche
@tasks_bp.route('', methods=['POST'])
@jwt_required()
def create_task():
    try:
        # Obtenir l'identité de l'utilisateur actuel
        user_id = get_jwt_identity()
        
        # Valider les données d'entrée
        schema = TaskSchema()
        data = schema.load(request.json)
        
        # Créer la nouvelle tâche
        new_task = Task(
            title=data['title'],
            description=data.get('description', ''),
            completed=data.get('completed', False),
            user_id=user_id
        )
        
        # Ajouter à la base de données
        db.session.add(new_task)
        db.session.commit()
        
        logger.info(f"Nouvelle tâche créée par l'utilisateur {user_id}: {new_task.title}")
        
        return jsonify({
            "message": "Tâche créée avec succès",
            "task": new_task.to_dict()
        }), 201
        
    except ValidationError as e:
        logger.warning(f"Validation error: {e.messages}")
        return jsonify({"error": e.messages}), 400
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Une erreur est survenue lors de la création de la tâche"}), 500

# Obtenir une tâche spécifique
@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    try:
        # Obtenir l'identité de l'utilisateur actuel
        user_id = get_jwt_identity()
        
        # Rechercher la tâche
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({"error": "Tâche non trouvée"}), 404
        
        return jsonify({"task": task.to_dict()}), 200
        
    except Exception as e:
        logger.error(f"Error getting task {task_id}: {str(e)}")
        return jsonify({"error": "Une erreur est survenue"}), 500

# Mettre à jour une tâche
@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    try:
        # Obtenir l'identité de l'utilisateur actuel
        user_id = get_jwt_identity()
        
        # Rechercher la tâche
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({"error": "Tâche non trouvée"}), 404
        
        # Valider les données d'entrée
        schema = TaskSchema()
        data = schema.load(request.json)
        
        # Mettre à jour la tâche
        task.title = data['title']
        task.description = data.get('description', task.description)
        task.completed = data.get('completed', task.completed)
        
        db.session.commit()
        
        logger.info(f"Tâche {task_id} mise à jour par l'utilisateur {user_id}")
        
        return jsonify({
            "message": "Tâche mise à jour avec succès",
            "task": task.to_dict()
        }), 200
        
    except ValidationError as e:
        logger.warning(f"Validation error: {e.messages}")
        return jsonify({"error": e.messages}), 400
    except Exception as e:
        logger.error(f"Error updating task {task_id}: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Une erreur est survenue lors de la mise à jour de la tâche"}), 500

# Supprimer une tâche
@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    try:
        # Obtenir l'identité de l'utilisateur actuel
        user_id = get_jwt_identity()
        
        # Rechercher la tâche
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({"error": "Tâche non trouvée"}), 404
        
        # Supprimer la tâche
        db.session.delete(task)
        db.session.commit()
        
        logger.info(f"Tâche {task_id} supprimée par l'utilisateur {user_id}")
        
        return jsonify({
            "message": "Tâche supprimée avec succès"
        }), 200
        
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Une erreur est survenue lors de la suppression de la tâche"}), 500

# Marquer une tâche comme terminée/non terminée
@tasks_bp.route('/<int:task_id>/toggle', methods=['PATCH'])
@jwt_required()
def toggle_task(task_id):
    try:
        # Obtenir l'identité de l'utilisateur actuel
        user_id = get_jwt_identity()
        
        # Rechercher la tâche
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({"error": "Tâche non trouvée"}), 404
        
        # Inverser l'état de complétion
        task.completed = not task.completed
        db.session.commit()
        
        status = "terminée" if task.completed else "non terminée"
        logger.info(f"Tâche {task_id} marquée comme {status} par l'utilisateur {user_id}")
        
        return jsonify({
            "message": f"Tâche marquée comme {status}",
            "task": task.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Error toggling task {task_id}: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Une erreur est survenue"}), 500

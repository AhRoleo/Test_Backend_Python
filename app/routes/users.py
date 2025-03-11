from flask import Blueprint, jsonify
from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from app.models.user import User
from app.schemas.user_schema import UserSchema

USER = Blueprint('users', __name__)

@USER.get('/me')
@jwt_required()
def get_user_info():
    """
    Fournir le détail d'un utilisateur connecté.

    Returns:
        200: Le détail de l'utilisateur qui a été identifié.
        400: Error.
    """
    current_user_identity = get_jwt_identity()
    
    current_user = User.query.filter_by(email=current_user_identity).first()
    if not current_user:
          current_user = User.query.filter_by(phone=current_user_identity).first()
    if not current_user:
            return jsonify({"status":"error",
                            "message": "Utilisateur non identifié"}), 409
    user_schema = UserSchema()
    return user_schema.dump(current_user)

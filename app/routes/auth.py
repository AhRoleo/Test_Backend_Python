from flask import Blueprint, jsonify
from flask import request
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError

from app import db
from app.models.user import User
from app.schemas.user_schema import UserSchema

import bcrypt

AUTH = Blueprint('auth', __name__)

@AUTH.post('/register')
def register():
    """
    Enregistrer un nouvel utilisateur.

    Returns:
        200: Utilisateur ajouté avec succès.
        400: Error.
        409: Identifiant déjà existant
    """
    try:
        # Valider et charger les données
        data = UserSchema().load(request.get_json())

        # Vérifier si l'email ou le numéro de téléphone existe déjà
        if "email" in data and User.query.filter_by(email=data["email"]).first():
                return jsonify({"status":"error",
                                "message": "Cet email existe déjà"}), 409
        elif "phone" in data and User.query.filter_by(phone=data["phone"]).first():
            return jsonify({"status":"error",
                            "message": "Ce numéro de téléphone existe déjà"}), 409

        # Hacher le password
        password = data.pop("password")
        new_user = User(**data)
        new_user.hash_password(password)

        # Ajouter l'utilisateur dans la base de données
        db.session.add(new_user)
        db.session.commit()

        user_schema = UserSchema()
        return jsonify({
            "message": "Utilisateur ajouté avec succès",
            "user": user_schema.dump(new_user)
        }), 200
    except ValidationError as e:
        return jsonify({"status": "error",
                        "message": e.messages}), 400
    except Exception as e:
        return jsonify({"status": "error",
                        "message": str(e)}), 400

@AUTH.post('/login')
def login():
    """
    Authentifier un utilisateur.

    Returns:
        200: Utilisateur authentifié avec succès.
        400: Error.
    """
    try:
        data = UserSchema().load(request.get_json())
        password = data.pop("password")

        format = {"email": "Email", "phone": "Numéro de téléphone"}
        identifier = "email" if "email" in data else "phone"

        # Vérifier si l'email ou le numéro de téléphone est valide
        user = User.query.filter(User.email == data[identifier]).first() if identifier == "email" else User.query.filter(User.phone == data[identifier]).first()
        if not user:
            return jsonify({"status": "error",
                            "message": f'{format[identifier]} incorrect'}), 400

        # Vérifier si le mot de passe est correct
        if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')) == False:
            return jsonify({"status": "error",
                            "message": "Mot de passe incorrect"}), 400
            
        # Générer un token
        access_token = create_access_token(identity=data[identifier])
        return  jsonify(access_token=access_token)
    except ValidationError as e:
        return jsonify({"status": "error",
                        "message": e.messages}), 400
    except Exception as e:
        return jsonify({"status": "error",
                        "message": str(e)}), 400

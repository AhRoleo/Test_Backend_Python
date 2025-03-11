from marshmallow import Schema, fields

class UserSchema(Schema):
    """Schéma pour valider un modèle User"""

    id = fields.Int(strict=True, dump_only=True)
    email = fields.Email()
    phone = fields.Str()
    password = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()

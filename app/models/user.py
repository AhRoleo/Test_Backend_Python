from app import db
from datetime import datetime, timezone
from sqlalchemy.sql import func
import bcrypt

class User(db.Model):
    """Model représentant l'utilisateur dans la base de données"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    email = db.Column(db.String(225), unique=True)
    phone = db.Column(db.String(225), unique=True)
    password_hash = db.Column(db.String(225))
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    first_name = db.Column(db.String(225))
    last_name = db.Column(db.String(225))

    def __repr__(self):
        return f"<User {self.email}>"

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

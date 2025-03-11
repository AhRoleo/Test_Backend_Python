from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

jwt = JWTManager()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root_password@mysql/database'
    app.config["JWT_SECRET_KEY"] = "secret-key"

    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.auth import AUTH
    from app.routes.users import USER
    app.register_blueprint(AUTH, url_prefix='/auth')
    app.register_blueprint(USER, url_prefix='/users')

    return app

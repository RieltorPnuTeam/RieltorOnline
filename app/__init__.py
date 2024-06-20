# app/__init__.py

from flask import Flask
from flask_migrate import Migrate
from config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        from .models import User
        db.create_all()

    # API registration
    from app.routes import bp
    app.register_blueprint(bp)

    from app.API.users_api import users_api_bp
    app.register_blueprint(users_api_bp)

    from app.API.apartments_api import apartments_api_bp
    app.register_blueprint(apartments_api_bp)

    from app.API.apartment_images_api import apartment_images_api_bp
    app.register_blueprint(apartment_images_api_bp)

    return app

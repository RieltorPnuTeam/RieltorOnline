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

    from app.routes import bp
    app.register_blueprint(bp)

    from app.api import api_bp
    app.register_blueprint(api_bp)

    return app

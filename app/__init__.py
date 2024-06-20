# app/__init__.py

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # Реєстрація Blueprint з веб-роутами
    from app.routes import bp
    app.register_blueprint(bp)

    # Реєстрація Blueprint з API
    from app.api import api_bp
    app.register_blueprint(api_bp)

    return app

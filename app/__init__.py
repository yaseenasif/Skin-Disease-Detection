from flask import Flask
from .config import Config
from .extensions import db, migrate, login_manager
from .models import models  # Import all models
from .routes import blueprints
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register Blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    # Use application context for creating tables in development
    with app.app_context():
        db.create_all()  # Create all tables

    return app


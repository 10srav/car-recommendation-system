"""
Flask Application Factory
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

def create_app(config_name='development'):
    """Create and configure the Flask application"""
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')

    # Load configuration
    from config.config import config
    app.config.from_object(config[config_name])

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    from app.models import db
    db.init_app(app)

    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

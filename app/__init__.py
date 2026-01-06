"""
Flask Application Factory
"""
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
import os
import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# Initialize extensions (will be bound to app in create_app)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

jwt = JWTManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()


def create_app(config_name='development'):
    """Create and configure the Flask application"""

    # Initialize Sentry for error tracking (production only)
    sentry_dsn = os.environ.get('SENTRY_DSN')
    if sentry_dsn and config_name == 'production':
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[FlaskIntegration()],
            traces_sample_rate=0.1,  # 10% of transactions for performance monitoring
            profiles_sample_rate=0.1,
            environment=config_name,
            send_default_pii=False  # Don't send personally identifiable information
        )

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

    # Initialize bcrypt for password hashing
    bcrypt.init_app(app)

    # Initialize CSRF protection for forms
    csrf.init_app(app)

    # Initialize JWT
    jwt.init_app(app)

    # Initialize token blacklist
    from app.token_blacklist import token_blacklist
    token_blacklist.init_app(app)

    # JWT token blocklist checker
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload.get('jti')
        return token_blacklist.is_blacklisted(jti)

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'success': False,
            'error': 'Token has expired',
            'error_code': 'token_expired'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'success': False,
            'error': 'Invalid token',
            'error_code': 'invalid_token'
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'success': False,
            'error': 'Authorization token is missing',
            'error_code': 'missing_token'
        }), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'success': False,
            'error': 'Token has been revoked',
            'error_code': 'token_revoked'
        }), 401

    # Initialize CORS - allow requests from any origin in dev, restrict in production
    if config_name == 'production':
        # In production, specify allowed origins via environment variable
        allowed_origins = os.environ.get('CORS_ORIGINS', '').split(',')
        allowed_origins = [o.strip() for o in allowed_origins if o.strip()]
        if allowed_origins:
            CORS(app, origins=allowed_origins, supports_credentials=True)
        else:
            CORS(app)  # Allow all if not configured (not recommended for production)
    else:
        CORS(app)  # Allow all origins in development

    # Initialize rate limiter
    limiter.init_app(app)

    # Initialize email service
    from app.email_service import init_mail
    init_mail(app)

    # Configure structured logging
    from app.logging_config import setup_logging, log_request
    setup_logging(app)
    log_request(app)

    # Register custom Jinja2 filters for car images
    from utils.car_images import get_car_image, get_thumbnail_url, get_large_url
    app.jinja_env.globals['get_car_image'] = get_car_image
    app.jinja_env.globals['get_thumbnail_url'] = get_thumbnail_url
    app.jinja_env.globals['get_large_url'] = get_large_url

    # Register blueprints
    from app.routes import main_bp
    from app.auth import auth_bp
    from app.api_docs import api_bp
    from app.admin import admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    # Pre-load ML models at startup (not on first request)
    # This prevents slow first requests and ensures models are ready
    if app.config.get('PRELOAD_ML_MODELS', True):
        with app.app_context():
            try:
                from app.ml_manager import ml_models
                ml_models.load_models()
                app.logger.info("ML models pre-loaded successfully")
            except Exception as e:
                app.logger.warning(f"Could not pre-load ML models: {e}")
                # Don't fail startup - models will load on first request

    return app

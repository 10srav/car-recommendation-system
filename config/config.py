# Configuration file for Flask app
# Contains all settings and configurations

import os
import secrets
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def get_secret_key():
    """Get secret key from environment or generate a warning for development"""
    secret = os.environ.get('SECRET_KEY')
    if secret:
        return secret
    # Generate a random key for development (changes on each restart)
    import warnings
    warnings.warn(
        "SECRET_KEY not set! Using random key. Set SECRET_KEY environment variable for production.",
        RuntimeWarning
    )
    return secrets.token_hex(32)


class Config:
    # Base configuration class
    SECRET_KEY = get_secret_key()
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(BASE_DIR, "automotive_marketplace.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    # ML Model preloading
    PRELOAD_ML_MODELS = True

    # Rate limiting defaults
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = "memory://"
    RATELIMIT_STRATEGY = "fixed-window"
    RATELIMIT_DEFAULT = "200 per day, 50 per hour"

    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

    # Upload folder for images
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # ML Models directory
    MODELS_DIR = os.path.join(BASE_DIR, 'models', 'trained_models')

    # Data directory
    DATA_DIR = os.path.join(BASE_DIR, 'data')

    # Pagination
    CARS_PER_PAGE = 12

    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # CSRF Protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour

    # Email configuration (for future implementation)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = False  # Set to True to see SQL queries


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Security settings for production
    SESSION_COOKIE_SECURE = True
    WTF_CSRF_SSL_STRICT = True
    
    # Enforce stronger secret key in production
    @property
    def SECRET_KEY(self):
        secret = os.environ.get('SECRET_KEY')
        if not secret or secret == 'dev-secret-key-change-in-production':
            raise ValueError("Production requires a secure SECRET_KEY environment variable")
        return secret
    
    # Database connection pool settings for production
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20,
    }


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key-for-testing-only'
    JWT_SECRET_KEY = 'test-jwt-secret-key-for-testing-only'
    PRELOAD_ML_MODELS = False
    RATELIMIT_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

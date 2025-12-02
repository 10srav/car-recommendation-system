# Production entry point for Flask app
# Run with: gunicorn -c gunicorn.conf.py wsgi:app

import os
import logging
from logging.handlers import RotatingFileHandler
from app import create_app
from app.models import db

# Determine environment
config_name = os.environ.get('FLASK_ENV', 'production')
app = create_app(config_name)

# Setup logging for production
if not app.debug:
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10240000,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('Car Recommendation System startup')

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()

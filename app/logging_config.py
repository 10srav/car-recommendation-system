"""
Structured logging configuration for the application
"""
import logging
import logging.handlers
import os
import sys
from datetime import datetime
import json


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""

    def format(self, record):
        log_record = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, 'request_id'):
            log_record['request_id'] = record.request_id
        if hasattr(record, 'user_id'):
            log_record['user_id'] = record.user_id
        if hasattr(record, 'ip_address'):
            log_record['ip_address'] = record.ip_address
        if hasattr(record, 'method'):
            log_record['method'] = record.method
        if hasattr(record, 'path'):
            log_record['path'] = record.path
        if hasattr(record, 'status_code'):
            log_record['status_code'] = record.status_code
        if hasattr(record, 'duration_ms'):
            log_record['duration_ms'] = record.duration_ms

        return json.dumps(log_record)


class RequestFormatter(logging.Formatter):
    """Formatter that includes request context"""

    def format(self, record):
        # Standard format with timestamp
        format_str = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'

        # Add request context if available
        extras = []
        if hasattr(record, 'request_id'):
            extras.append(f"request_id={record.request_id}")
        if hasattr(record, 'user_id'):
            extras.append(f"user_id={record.user_id}")
        if hasattr(record, 'ip_address'):
            extras.append(f"ip={record.ip_address}")

        if extras:
            format_str = f'%(asctime)s - %(levelname)s - [{", ".join(extras)}] - %(name)s - %(message)s'

        self._style._fmt = format_str
        return super().format(record)


def setup_logging(app):
    """Configure application logging"""

    # Get log level from config
    log_level = app.config.get('LOG_LEVEL', 'INFO')
    log_file = app.config.get('LOG_FILE', 'logs/app.log')
    use_json = app.config.get('LOG_JSON_FORMAT', False)

    # Ensure log directory exists
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Remove default handlers
    app.logger.handlers = []

    # Create formatters
    if use_json:
        formatter = JSONFormatter()
    else:
        formatter = RequestFormatter(
            '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)

    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    # Set the logger level
    app.logger.setLevel(log_level)

    # Also configure werkzeug and sqlalchemy loggers
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

    app.logger.info('Logging configured successfully', extra={
        'log_level': log_level,
        'log_file': log_file,
        'json_format': use_json
    })


def get_request_logger(app):
    """Get a logger that includes request context"""
    from flask import request, g
    import uuid

    class RequestContextFilter(logging.Filter):
        def filter(self, record):
            # Add request context to log records
            try:
                record.request_id = getattr(g, 'request_id', '-')
                record.user_id = getattr(g, 'user_id', '-')
                record.ip_address = request.remote_addr if request else '-'
                record.method = request.method if request else '-'
                record.path = request.path if request else '-'
            except RuntimeError:
                # Outside request context
                record.request_id = '-'
                record.user_id = '-'
                record.ip_address = '-'
                record.method = '-'
                record.path = '-'
            return True

    # Add filter to all handlers
    for handler in app.logger.handlers:
        handler.addFilter(RequestContextFilter())

    return app.logger


def log_request(app):
    """Decorator/middleware to log requests"""
    from flask import request, g
    import time
    import uuid

    @app.before_request
    def before_request():
        g.request_id = str(uuid.uuid4())[:8]
        g.start_time = time.time()
        app.logger.info(f"Request started: {request.method} {request.path}", extra={
            'request_id': g.request_id,
            'method': request.method,
            'path': request.path,
            'ip_address': request.remote_addr
        })

    @app.after_request
    def after_request(response):
        duration = (time.time() - g.start_time) * 1000  # Convert to ms
        app.logger.info(f"Request completed: {response.status_code}", extra={
            'request_id': getattr(g, 'request_id', '-'),
            'status_code': response.status_code,
            'duration_ms': round(duration, 2)
        })
        # Add request ID to response headers for tracing
        response.headers['X-Request-ID'] = getattr(g, 'request_id', '-')
        return response

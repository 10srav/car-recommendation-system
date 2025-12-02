# ===========================================
# Gunicorn Configuration for Production
# ===========================================
# Usage: gunicorn -c gunicorn.conf.py run:app

import multiprocessing
import os

# Server socket
bind = os.getenv('GUNICORN_BIND', '0.0.0.0:5000')
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'  # Use 'gevent' for async
worker_connections = 1000
timeout = 120
keepalive = 5

# Process naming
proc_name = 'car-recommendation-system'

# Server mechanics
daemon = False
pidfile = '/tmp/gunicorn.pid'
user = None
group = None
tmp_upload_dir = None

# Logging
errorlog = 'logs/gunicorn-error.log'
accesslog = 'logs/gunicorn-access.log'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# SSL Configuration (uncomment for HTTPS)
# keyfile = '/path/to/key.pem'
# certfile = '/path/to/cert.pem'

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Graceful timeout
graceful_timeout = 30

# Restart workers after this many requests (helps prevent memory leaks)
max_requests = 1000
max_requests_jitter = 50

# Preload app for faster worker startup
preload_app = True

def on_starting(server):
    """Called just before the master process is initialized."""
    print("Starting Gunicorn server...")

def on_exit(server):
    """Called just before exiting Gunicorn."""
    print("Shutting down Gunicorn server...")

def worker_int(worker):
    """Called when a worker receives SIGINT or SIGQUIT."""
    print(f"Worker {worker.pid} interrupted")

def worker_abort(worker):
    """Called when a worker receives SIGABRT."""
    print(f"Worker {worker.pid} aborted")

import os
import multiprocessing

# Server socket
bind = '0.0.0.0:' + os.environ.get('PORT', '10000')

# Worker processes
workers = min(multiprocessing.cpu_count() * 2 + 1, 4)  # Optimized worker count
worker_class = 'gevent'  # Using gevent for better I/O handling
worker_connections = 1000

# Timeouts
timeout = 120
keepalive = 5

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Server mechanics
preload_app = True
max_requests = 1000
max_requests_jitter = 200

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Performance
max_requests = 1000
max_requests_jitter = 200
worker_tmp_dir = '/dev/shm'  # Use shared memory for worker temp files

# Debugging
reload = os.environ.get('FLASK_ENV') == 'development'

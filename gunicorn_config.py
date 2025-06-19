import os

# Server socket
bind = '0.0.0.0:' + os.environ.get('PORT', '10000')

# Worker processes
workers = 2
worker_class = 'sync'
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
max_requests_jitter = 50

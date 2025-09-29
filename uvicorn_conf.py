from app.core.config import get_settings

settings = get_settings()

bind = f'{settings.host}:{settings.port}'
workers = settings.workers
worker_class = 'uvicorn.workers.UvicornWorker'
worker_connections = 1000
max_requests = 10000
max_requests_jitter = 1000
timeout = 30
keepalive = 2
preload_app = True

accesslog = '-'
errorlog = '-'
loglevel = settings.log_level.lower()
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

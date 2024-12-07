bind = "127.0.0.1:4000"
pidfile = "parent.pid"
workers = 1
worker_class = "sync"
worker_connections = 1000
loglevel = "info"
accesslog = "access.log"
errorlog = "server.log"

import multiprocessing

# Binding
bind = "0.0.0.0:5000"

# Workers: 2 × CPUs + 1, máximo 4 para evitar explosión en máquinas con muchos cores
workers = 2
worker_class = "sync"

# Timeouts
timeout = 30
keepalive = 5

# Logging a stdout → Docker los captura con `docker logs`
accesslog = "-"
errorlog  = "-"
loglevel  = "info"

# Graceful restart
graceful_timeout = 30

#!/usr/bin/env bash
set -e

# Espera opcional
WAIT=${WAIT_FOR:-0}
if [ "$WAIT" -gt 0 ]; then
  echo "Esperando $WAIT segundos..."
  sleep "$WAIT"
fi

# carregar .env se existir
if [ -f "/app/.env" ]; then
  export $(grep -v '^#' /app/.env | xargs)
fi

# se DB_HOST=db (docker) espera o Postgres
if [ -n "$DB_HOST" ] && [ "$DB_HOST" = "db" ]; then
  echo "Aguardando o banco (DB_HOST=db)..."
  i=0
  until nc -z ${DB_HOST} ${DB_PORT:-5432} || [ $i -gt 30 ]; do
    echo "Aguardando db... ($i)"
    i=$((i+1))
    sleep 1
  done
fi

# Detectar FastAPI (main:app)
python - <<'PY' 2>/dev/null
import importlib,sys
try:
    m = importlib.import_module("main")
    if hasattr(m,"app"):
        sys.exit(0)
    else:
        sys.exit(1)
except Exception:
    sys.exit(1)
PY
if [ $? -eq 0 ]; then
  echo "Iniciando com uvicorn main:app"
  exec uvicorn main:app --host 0.0.0.0 --port 5000
fi

# Se existir app.py (Flask)
if [ -f "/app/app.py" ]; then
  echo "Iniciando Flask (app.py)"
  export FLASK_APP=app.py
  exec flask run --host=0.0.0.0 --port=5000
fi

# fallback: se existir run.py
if [ -f "/app/run.py" ]; then
  echo "Iniciando run.py"
  exec python run.py
fi

echo "Nenhuma aplicação detectada (main:app, app.py ou run.py). Saindo."
exit 1

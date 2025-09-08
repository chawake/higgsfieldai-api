#!/bin/sh

# Wait for the database to be reachable before running migrations
echo "Waiting for database ${DB_HOST:-db}:${DB_PORT:-5432}..."
retries=30
while ! python - <<'PY'
import os, socket
host = os.environ.get('DB_HOST', 'db')
port = int(os.environ.get('DB_PORT', '5432'))
s = socket.socket()
s.settimeout(2)
try:
    s.connect((host, port))
    print('ok')
except Exception as e:
    raise SystemExit(1)
finally:
    s.close()
PY
do
  retries=$((retries-1))
  if [ "$retries" -le 0 ]; then
    echo "Database is not reachable. Exiting." >&2
    exit 1
  fi
  sleep 2
done

alembic upgrade head
gunicorn src.main:app -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8080 --forwarded-allow-ips="*"

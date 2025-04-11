#!/bin/bash
set -e

export DATABASE_URL="mysql+pymysql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT:-3306}/${DB_NAME}?charset=utf8mb4"

check_db_connection() {
    local max_retries=30
    local retry_delay=2
    
    for ((i=1; i<=max_retries; i++)); do
        if python -c "
import pymysql
try:
    conn = pymysql.connect(
        host='${DB_HOST}',
        port=${DB_PORT:-3306},
        user='${DB_USER}',
        password='${DB_PASSWORD}',
        db='${DB_NAME}'
    )
    conn.close()
    print('✓ Conexión exitosa a MySQL (Intento {}/{}))'.format($i, $max_retries))
    exit(0)
except pymysql.MySQLError as e:
    print('✗ Intento {}/{}: Error de conexión - {}'.format($i, $max_retries, e))
    exit(1)
"; then
            return 0
        fi
        sleep $retry_delay
    done
    echo "✗ No se pudo conectar a MySQL después de $max_retries intentos"
    return 1
}

echo "Esperando a que la base de datos esté lista..."
check_db_connection || exit 1

echo "Aplicando migraciones de base de datos..."
alembic upgrade head

echo "Iniciando la aplicación FastAPI..."
exec fastapi run src/main.py --host 0.0.0.0 --port 80
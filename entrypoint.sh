#!/bin/sh

# Ожидаем, пока БД поднимется (опционально). Можно реализовать простой цикл ожидания:
if [ -n "$POSTGRES_HOST" ]; then
  echo "Waiting for postgres at $POSTGRES_HOST:$POSTGRES_PORT..."
  # Попробуем несколько раз подключиться
  RET=1
  while [ $RET -ne 0 ]; do
    sleep 1
    echo "Checking database connection..."
    # Попытка подключиться через psql; нужна утилита psql, но в slim-образе её может не быть.
    # Вместо этого можно попытаться через Python:
    python3 - <<EOF
import sys, psycopg2, os
try:
    conn = psycopg2.connect(
        dbname=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD'),
        host=os.environ.get('POSTGRES_HOST'),
        port=os.environ.get('POSTGRES_PORT', 5432),
        connect_timeout=1
    )
    conn.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
EOF
    RET=$?
  done
  echo "PostgreSQL is up"
fi

# Применяем миграции
echo "Apply database migrations"
python manage.py migrate --noinput

# Собираем статические файлы
echo "Collect static files"
python manage.py collectstatic --noinput

# Создание суперпользователя, если его нет
echo "Создание суперпользователя (если отсутствует)..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("Суперпользователь admin создан.")
else:
    print("Суперпользователь admin уже существует.")
END

# Запуск Gunicorn
echo "Starting Gunicorn"
# Если вы хотите использовать настройки Gunicorn, можно здесь добавить параметры: --workers, --bind, др.
gunicorn smartzhkh.wsgi:application --bind 0.0.0.0:8000

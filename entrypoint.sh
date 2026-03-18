#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--> Rodando migrações do banco de dados..."
python manage.py migrate --noinput

echo "--> Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "--> Iniciando Gunicorn na porta ${PORT:-8000}..."
exec gunicorn --bind 0.0.0.0:${PORT:-8000} core.wsgi:application

python manage.py createsuperuser --noinput --username admin --email [admin@admin.com] --password Adv@2026

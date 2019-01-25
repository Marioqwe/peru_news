#!/bin/bash

# wait for PostgreSQL server to start
sleep 10

python manage.py makemigrations --verbosity 0
python manage.py migrate --verbosity 0

if [ "$DJANGO_ENV" = 'production' ]; then
    python manage.py collectstatic --noinput

    echo "Running Production Server"
    gunicorn app.config.wsgi:application \
             --bind 0.0.0.0:8000 \
             --workers 3 \
             --log-level=warning
else # default to development.
    echo "Running Development Server"
    python manage.py runserver 0.0.0.0:8000
fi
#!/bin/sh

# Healthcheck database server
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# python manage.py flush --no-input
# python manage.py migrate

exec "$@"

# Register cronjobs
python manage.py crontab add

# List cronjobs
crontab -l

# Start cron service
crond

# Start web server
gunicorn sw.wsgi:application --bind 0.0.0.0:8000

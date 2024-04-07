#!/bin/sh

service postgresql start

echo "Waiting for postgres..."

while ! nc -z localhost 5432; do
  sleep 1
done

echo "PostgreSQL started"

su - postgres -c "psql -c \"SELECT 1 FROM pg_roles WHERE rolname='$POSTGRES_USER'\" | grep -q 1 || psql -c \"CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';\""
su - postgres -c "psql -c \"SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB'\" | grep -q 1 || psql -c \"CREATE DATABASE $POSTGRES_DB OWNER $POSTGRES_USER;\""

python manage.py makemigrations
python manage.py migrate
python manage.py parsetable songs.json

DJANGO_SUPERUSER_USERNAME=$DJANGO_USER \
DJANGO_SUPERUSER_PASSWORD=$DJANGO_PASSWORD \
DJANGO_SUPERUSER_EMAIL="test@test.ru" \
python manage.py createsuperuser --noinput

python manage.py runserver 0.0.0.0:8000

exec "$@"
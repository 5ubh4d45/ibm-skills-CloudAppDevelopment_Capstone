#!/bin/sh

# if there is a postgres container running, wait for it to be ready
if ["$DATABASE" = "postgres"]; then
    echo "Waiting for postgres..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
        sleep 0.1
    done

    echo "PostgresSQL started"
fi

# make migrations and migrate the database
echo "Making migrations and migrating the database..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

exec "$@"
#!/bin/bash
set -e

# If you don't have a Django project, create one (optional, for a fresh start).
# If you already have a project, remove these lines.
if [ ! -f "/app/myproject/manage.py" ]; then
    django-admin startproject myproject
    chmod -R 777 /app/myproject
fi

cd myproject
# Run migrations to set up the database
python manage.py migrate

# Start Django's development server
# NOTE: No --noreload here, so Django will watch for code changes!
exec python manage.py runserver 0.0.0.0:8000

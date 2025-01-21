#!/bin/bash
set -e

# Move into your Django project directory
cd /app

# If you don't have a Django project, create one (optional, for a fresh start).
# If you already have a project, remove these lines.
if [ ! -f "/app/myproject/manage.py" ]; then
    django-admin startproject myproject
fi

cd /app/myproject

# # (Optional) If you need to create an app automatically—again, remove if you already have one.
# if [ ! -d "/app/myproject/myapp" ]; then
#     python manage.py startapp myapp
# fi

# # Run migrations to set up the database
# python manage.py migrate

# Start Django's development server
# NOTE: No --noreload here, so Django will watch for code changes!
exec python manage.py runserver 0.0.0.0:8000

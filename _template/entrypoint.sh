#!/bin/bash
# set -e  # Commented out for Windows compatibility

# If the Django project folder doesn't exist, create it.
# Remove this if you already have a "myproject" folder on your host.
if [ ! -f "/usr/src/app/myproject/manage.py" ]; then
    django-admin startproject myproject
fi

# Go into the project directory
cd myproject

# Run Django migrations
python manage.py migrate

# Start Django development server on 0.0.0.0:8000
exec python manage.py runserver 0.0.0.0:8000

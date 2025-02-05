# Setup
```sh
docker stop django_project
docker rm django_project
docker-compose up --build
```

# Go inside container
```sh
docker-compose exec web bash
```

# Create App
```sh
docker-compose exec web bash
cd myproject
python manage.py createsuperuser
python manage.py startapp myapp
```
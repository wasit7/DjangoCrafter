# Django template2
Below is a **complete template** for a Docker-based Django project that includes PostgreSQL, JupyterLab, and the **django-extensions** package for creating class diagrams (and other helpful development tools). This setup will help you quickly spin up a Django environment where you can develop, diagram your models, and test database interactions.

---

## **1. `docker-compose.yml`**

```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    container_name: django_postgres
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=django_db
      - POSTGRES_USER=django_user
      - POSTGRES_PASSWORD=django_pass
    ports:
      - "5432:5432"
    restart: unless-stopped

  web:
    build: .
    container_name: django_project
    volumes:
      - .:/usr/src/app:rw
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
      - POSTGRES_DB=django_db
      - POSTGRES_USER=django_user
      - POSTGRES_PASSWORD=django_pass
      - POSTGRES_HOST=db
    depends_on:
      - db
    command: /bin/bash /usr/src/app/entrypoint.sh

  jupyter:
    build: .
    container_name: django_jupyter
    command: >
      bash -c "
      pip install --no-cache-dir jupyterlab &&
      jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.token=''
      "
    volumes:
      - .:/usr/src/app:rw
    ports:
      - "8888:8888"
    environment:
      - PYTHONUNBUFFERED=1
    depends_on:
      - db

volumes:
  db_data:
```

### **Key Points**

- **db**: Runs PostgreSQL, storing data in the `db_data` volume.  
- **web**: Builds from the local `Dockerfile`, mounts the project directory, and runs Django with an `entrypoint.sh`.  
- **jupyter**: Installs JupyterLab on startup so you can open notebooks at `http://localhost:8888`.  
- **Environment Variables**: `POSTGRES_*` details are used by Django to connect to PostgreSQL.  
- **Volumes**: Data persists in `db_data`, so you won’t lose it when restarting containers.

---

## **2. `Dockerfile`**

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a working directory
WORKDIR /usr/src/app

# Copy requirements first for caching
COPY requirements.txt /usr/src/app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . /usr/src/app/

# Make entrypoint script executable
RUN chmod +x /usr/src/app/entrypoint.sh

# Expose Django’s default port
EXPOSE 8000

# Default command
CMD ["/usr/src/app/entrypoint.sh"]
```

### **Key Points**

- Installs any required system packages for building Python dependencies (`libpq-dev` for PostgreSQL).  
- Caches `requirements.txt` first, speeding up rebuilds when your dependencies haven’t changed.  
- Copies the rest of your code into `/usr/src/app`.  
- Makes the `entrypoint.sh` script executable.  
- Exposes port 8000 for Django.

---

## **3. `entrypoint.sh`**

```bash
#!/bin/bash
set -e

# Optional: Create a Django project if it doesn't exist.
# If you already have a Django project in this repo, remove or adjust this section.
if [ ! -f "/usr/src/app/myproject/manage.py" ]; then
    django-admin startproject myproject
fi

cd myproject

# If you'd like to automatically configure the DB settings, you can add sed commands here.
# For now, we assume you're manually configuring settings.py to use PostgreSQL.

# Run migrations
python manage.py migrate

# Start Django dev server
exec python manage.py runserver 0.0.0.0:8000
```

### **Key Points**

- **set -e**: Fails script on any command error (remove/comment for Windows compatibility if needed).  
- If your code base already has a Django project, remove the `django-admin startproject` part.  
- Automatically runs `migrate` to set up database tables.  
- Launches the Django development server at `0.0.0.0:8000`.

---

## **4. `requirements.txt`**

Below is a **minimal** set of dependencies to work with Django, PostgreSQL, Django Extensions, and JupyterLab. Adjust versions as needed:

```plaintext
Django==4.2
psycopg2-binary==2.9.6
django-extensions==3.2.3

# For exploring data in notebooks (if you prefer to install them here rather than at runtime)
jupyterlab==4.0.2

# Optionally, add other libraries:
# tailwindcss, whitenoise, or anything else you use in your project
```

### **Key Points**

- **Django**: The main framework.  
- **psycopg2-binary**: Allows Django to connect to PostgreSQL.  
- **django-extensions**: Provides extra commands (including `graph_models` for class diagrams).  
- **jupyterlab**: If you prefer installing it here rather than in the container command.  
- Pin versions (like `==4.2`) to ensure consistent builds.

---

## **PostgreSQL Configuration in `settings.py`**

In `myproject/settings.py` (or wherever your project’s settings are), configure the default database to PostgreSQL using the environment variables:

```python
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', 'django_db'),
        'USER': os.environ.get('POSTGRES_USER', 'django_user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'django_pass'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': '5432',
    }
}

# Add "django_extensions" to INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    'django_extensions',
    # ...
]
```

---

## **How to Generate a Class Diagram**

Once your models are defined and **django-extensions** is in `INSTALLED_APPS`:

1. **Launch Containers**:  
   ```bash
   docker-compose up --build
   ```
2. **Open a Shell**:  
   In another terminal, run:
   ```bash
   docker-compose exec web bash
   ```
   This drops you into the `web` container shell.
3. **Generate Diagram**:  
   Inside the container, if your Django project folder is `myproject`, run:
   ```bash
   cd myproject
   python manage.py graph_models -a -g -o diagram.png
   ```
   - `-a` = All apps  
   - `-g` = Group models by app  
   - `-o diagram.png` = Output file name  
4. **View the Diagram**:  
   A `diagram.png` file will appear in the same folder. You can view or download it locally to see the relationships among your models.

---

## **Usage Instructions**

1. **Build & Run**:  
   ```bash
   docker-compose build
   docker-compose up
   ```
   - The database (PostgreSQL), Django, and JupyterLab containers will start.

2. **Django**:  
   - View the Django app at [http://localhost:8000](http://localhost:8000).  
   - The `entrypoint.sh` script creates a `myproject` folder if it doesn’t exist, runs migrations, and starts the dev server.

3. **JupyterLab**:  
   - Access JupyterLab at [http://localhost:8888](http://localhost:8888).  
   - No token is required (for local dev convenience). Once in, you can open notebooks, run Python code that references your project’s files, and even manipulate your Django models.

4. **Persisting Data**:  
   - The PostgreSQL container uses a named volume `db_data`. Data is preserved across container restarts.

5. **Stop Containers**:  
   ```bash
   docker-compose down
   ```
   - This stops and removes containers, but leaves the `db_data` volume intact.

---

## **Customizations**

- **Production**:  
  - For production, you might run Django with `gunicorn` or `uwsgi` behind an Nginx proxy, secure Jupyter, and store environment variables more securely (e.g., `.env` files or Docker secrets).
- **Additional Libraries**:  
  - Add or remove dependencies in `requirements.txt` to fit your project’s needs (e.g., DRF, tailwind, etc.).
- **Version Pinning**:  
  - Carefully pin package versions in `requirements.txt` to avoid unexpected updates.

---

### **Conclusion**

With these four files—`docker-compose.yml`, `Dockerfile`, `entrypoint.sh`, and `requirements.txt`—plus minor configurations in **Django settings**, you have a fully functional environment to **develop, diagram, and test** your Django application with PostgreSQL and **django-extensions**. This setup is ideal for **classroom demonstrations**, local community projects, or personal learning, allowing you to seamlessly generate class diagrams and manage your data in a containerized, reproducible manner.
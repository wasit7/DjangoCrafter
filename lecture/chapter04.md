## **Chapter 4: Django**

In this chapter, we dive into the **Django** web framework, exploring its core architecture and how it leverages the **Model-View-Template (MVT)** pattern. By the end of this chapter, students will be able to create and run a Django project, configure its settings, and understand how Django processes requests using views and templates.

---

### **1. Theories**

1. **Django’s MVT Architecture**  
   - **Model**: Describes data in Python classes. Each model corresponds to a database table.  
   - **View**: Handles requests and returns responses, often rendering a template or returning JSON.  
   - **Template**: The front-end presentation layer, usually HTML files with placeholder variables.  
   - **Comparison to MVC**: Django’s “view” is closer to what many frameworks call a “controller,” while Django’s “template” is the view layer in traditional MVC.

2. **Django Project vs. App**  
   - **Project**: The main container with `manage.py`, `settings.py`, `urls.py`, `wsgi.py`, etc.  
   - **App**: A smaller component of functionality (e.g., `myapp`) that you can plug into different projects.  
   - **Multiple Apps**: Typical Django projects split functionality across multiple apps (e.g., `accounts`, `blog`, `shop`).

3. **URLs and Views**  
   - **Project-level `urls.py`**: Usually references global routes (e.g., `admin/`) and includes app-level URLs.  
   - **App-level `urls.py`** (optional): Defines routes specific to that app. You’ll typically do `path('myapp/', include('myapp.urls'))` at the project level.  
   - **View Functions**: Python functions or class-based views that process requests and either render a template or return data (e.g., JSON for an API).

4. **Django Settings and Environment Variables**  
   - **DATABASES**: Typical configuration for PostgreSQL or other databases. You can read environment variables (like `os.environ.get("POSTGRES_DB")`).  
   - **DEBUG and SECRET_KEY**: Often set via `.env` or Docker Compose to avoid hardcoding secrets in code.  
   - **INSTALLED_APPS**: Lists default Django apps plus any custom or third-party apps.

5. **Running Django in Docker**  
   - **Dockerfile**: Often `FROM python:3.9-slim`. Installs Django via a requirements file.  
   - **docker-compose.yml**:  
     ```yaml
     services:
       web:
         build: .
         ports:
           - "8000:8000"
         environment:
           - DEBUG=1
         command: python manage.py runserver 0.0.0.0:8000
     ```
   - **Migrations**: Run `python manage.py migrate` inside the container to set up the database.

---

### **2. Step-by-Step Workshop**

#### **Step 1: Create a Django Project**

1. **Install Django**  
   - Locally or in a container’s `requirements.txt`:  
     ```plaintext
     Django==4.2
     ```
2. **Start a Project**  
   ```bash
   docker compose run --rm web django-admin startproject myproject .
   ```
   - Assumes `web` is your service name and the current directory is where you want to create `manage.py` and the `myproject/` folder.

3. **Directory Layout**  
   - You’ll see:
     ```
     manage.py
     myproject/
       __init__.py
       asgi.py
       settings.py
       urls.py
       wsgi.py
     ```

#### **Step 2: Edit `settings.py` for Docker Integration**

1. **DATABASES** Example  
   ```python
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
   ```
2. **DEBUG and Allowed Hosts**  
   ```python
   DEBUG = bool(int(os.environ.get('DEBUG', 1)))
   ALLOWED_HOSTS = ['*']
   ```
   - This approach uses `DEBUG=1` or `DEBUG=0` from environment variables.

3. **INSTALLED_APPS**  
   ```python
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       # Add your custom apps here, e.g. 'myapp'
   ]
   ```

#### **Step 3: Basic URLs and Views**

1. **Project-Level `urls.py`**  
   ```python
   from django.contrib import admin
   from django.urls import path

   urlpatterns = [
       path('admin/', admin.site.urls),
   ]
   ```
2. **App-Level `urls.py`** (optional)  
   - If you have an app named `myapp`, create `myapp/urls.py`:
     ```python
     from django.urls import path
     from .views import home

     urlpatterns = [
         path('', home, name='home'),
     ]
     ```
   - Include in project `urls.py`:
     ```python
     from django.urls import path, include

     urlpatterns = [
       path('admin/', admin.site.urls),
       path('myapp/', include('myapp.urls')),
     ]
     ```

#### **Step 4: Run the Development Server**

1. **Migrations**  
   ```bash
   docker compose run web python manage.py migrate
   ```
2. **Create Superuser (Optional)**  
   ```bash
   docker compose run web python manage.py createsuperuser
   ```
3. **Start the Server**  
   ```bash
   docker compose up -d
   ```
   - Check `http://localhost:8000`.

#### **Step 5: Checking Logs and Stopping**

1. **Logs**  
   ```bash
   docker compose logs -f web
   ```
2. **Stop**  
   ```bash
   docker compose down
   ```
   - Containers are removed. Any named volumes for the database remain unless removed.

---

### **3. Assignment**

1. **Objective**  
   - Demonstrate you can set up a basic Django project in Docker, configure environment-based settings, and serve a simple view.

2. **Tasks**  
   1. **Initialize a Django Project**  
      - Use `django-admin startproject` in a container or local environment.  
      - Confirm `manage.py`, `settings.py`, etc. are created.
   2. **Setup Database and Docker Compose**  
      - Configure `DATABASES` in `settings.py` to read from environment variables.  
      - Use a `db` service (e.g., Postgres) if available, or stick to SQLite for simplicity.
   3. **Add a Simple View**  
      - Create a `views.py` with a function returning “Hello, Django in Docker!”  
      - Map it to a path in `urls.py`.
   4. **Screenshot**  
      - Show your browser displaying the message at `http://localhost:8000`.

3. **Deliverables**  
   - **docker-compose.yml** snippet showing the `web` service.  
   - **Short Explanation** of how `ALLOWED_HOSTS` and `DEBUG` are controlled by environment variables.  
   - **Screenshot** of your running page.

---

### **4. Conclusion**

**Django** provides a robust, “batteries-included” framework for building scalable web applications. Its **MVT** architecture organizes data, logic, and presentation cleanly. By containerizing Django with **Docker**, you gain reliable, portable environments that seamlessly integrate with other services like PostgreSQL or Redis. Mastering the basics of project structure, environment-specific settings, and running the dev server in Docker sets a strong foundation for advanced Django features (models, admin, caching, etc.) in future chapters.
# week05 Tutorial
<img src="https://raw.githubusercontent.com/wasit7/DjangoCrafter/refs/heads/main/week07/Screenshot%20from%202025-04-09%2023-57-29.png" width="30%">
<img src="https://raw.githubusercontent.com/wasit7/DjangoCrafter/refs/heads/main/week07/Screenshot%20from%202025-04-09%2023-56-22.png" width="30%">
<img src="https://raw.githubusercontent.com/wasit7/DjangoCrafter/refs/heads/main/week07/Screenshot%20from%202025-04-09%2023-56-28.png" width="30%">
<img src="https://raw.githubusercontent.com/wasit7/DjangoCrafter/refs/heads/main/week07/Screenshot%20from%202025-04-09%2023-57-18.png" width="30%">


# note

### Project Overview
- **Goal**: Build a bike rental web app with Django, featuring a home page, bike list, and bike detail pages.
- **Tech Stack**: Django (Python), PostgreSQL (via Docker), Tailwind CSS (CDN), Noto Sans Thai font (Google Fonts).
- **Environment**: Docker Compose with `web` (Django) and `db` (PostgreSQL) services.

---

### Key Steps

1. **Setup & Models**:
   - Created `Bike` model (`name`, `hourly_rate`, `description`, `is_available`, `image`) and `Rental` model.
   - Added image upload functionality with `ImageField` and configured media settings.

2. **Docker Configuration**:
   - Defined `docker-compose.yml` with `db` (Postgres) and `web` (Django) services.
   - Added `entrypoint.sh` to initialize the project and run migrations.
   - Created a superuser via `docker-compose exec web python manage.py createsuperuser`.

3. **Views & URLs**:
   - **Home Page**: Function-Based View (`home`) at `/`.
   - **Bike List**: Class-Based `ListView` (`BikeListView`) at `/bikes/`, sorted by `hourly_rate` descending, with search by `name` and `description`.
   - **Bike Detail**: Class-Based `DetailView` (`BikeDetailView`) at `/bikes/<pk>/`.
   - URLs mapped in `myapp/urls.py` and included in `myproject/urls.py`.

4. **Templates**:
   - **Base Template (`base.html`)**:
     - Added Tailwind CSS via CDN and Noto Sans Thai font.
     - Designed a Facebook-like navbar (`bg-blue-600`) and footer (`bg-gray-100`, `text-gray-700`).
     - Included navigation (“หน้าแรก” and “จักรยาน”) and a footer with Thai text.
   - **Home (`home.html`)**: Welcome message and link to bike list.
   - **Bike List (`bike_list.html`)**: Grid layout (`grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4`) with search form.
   - **Bike Detail (`bike_detail.html`)**: Displays bike details with image and availability.

5. **Styling**:
   - Used Tailwind CSS for responsive design.
   - Adjusted colors to be web-safe (sRGB gamut): `bg-blue-600` (navbar), `bg-gray-100` (body/footer), `text-gray-700` (footer text).
   - Applied Thai text (e.g., “เช่าจักรยาน”, “ค้นหา”) with Noto Sans Thai font.

6. **Features**:
   - **Search**: Added to `BikeListView` to filter bikes by `name` or `description`.
   - **Sorting**: Modified `BikeListView` to sort by `hourly_rate` descending.

---

### Final Structure
```
/myproject/
  /myapp/
    /templates/myapp/
      base.html
      home.html
      bike_list.html
      bike_detail.html
    models.py
    views.py
    urls.py
  /myproject/
    settings.py
    urls.py
  docker-compose.yml
  entrypoint.sh
```

---

### Running the App
- Start: `docker-compose up -d`
- URLs:
  - Home: `http://localhost:8000/`
  - Bike List: `http://localhost:8000/bikes/`
  - Bike Detail: `http://localhost:8000/bikes/<pk>/`
- Admin: `http://localhost:8000/admin/` (use superuser credentials).

---

### Highlights
- **Responsive**: Grid layout adapts to screen sizes.
- **Thai Support**: Noto Sans Thai font ensures proper rendering.
- **Facebook-like**: Blue navbar and light gray footer, adjusted for sRGB safety.
- **Functionality**: Image uploads, search, and sorting enhance usability.

# setup

```sh
cp -rp _template2 week04
cd wee04
docker compose up
```

# create an app
- create app
```
python manage.py startapp myapp
chmor -R 777 .
```

- from week03 get admin.py and models.py
- got to jupyter terminal

# settings.py
```
#settings.py
INSTALLED_APPS = [
    ...
    'django_extensions',
    'myapp'
]
```

# test notebook
```
# notebook.ipynb
from asgiref.sync import sync_to_async
from myapp.models import Bike

async def fetch_all_bikes():
    bikes = await sync_to_async(list)(Bike.objects.all())
    return bikes

# Directly await the coroutine in an async cell
all_bikes = await fetch_all_bikes()
print(all_bikes)
```

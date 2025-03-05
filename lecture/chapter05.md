## **Chapter 5: Django Models**

In this chapter, we focus on **Django Models**, which form the backbone of how data is structured and managed in Django. You will learn how models map to database tables, how to define fields and relationships, and how to apply migrations to keep your schema in sync with your code. By the end, students should be able to create custom model classes, run queries via the ORM, and understand best practices for model design.

---

### **1. Theories**

1. **Models in Django**  
   - **Definition**: A model is a Python class that inherits from `django.db.models.Model`. Each attribute corresponds to a database column.  
   - **Mapping**: Django’s ORM automatically translates these class definitions into SQL CREATE TABLE or ALTER TABLE statements when migrations are run.  
   - **Encapsulation**: Business logic related to data (validation, calculated fields) can be placed within model methods (e.g., `save()` overrides).

2. **Fields and Relationships**  
   - **Common Field Types**:  
     - `CharField`: For short text (e.g., `name`).  
     - `TextField`: For long text.  
     - `IntegerField`: For integers.  
     - `DecimalField`: For monetary or precise numeric data (with `max_digits` and `decimal_places`).  
     - `DateTimeField`: For timestamps.  
     - `BooleanField`: True/False values.  
   - **Relationships**:  
     - `ForeignKey(Model, on_delete=...)`: Many-to-one.  
     - `ManyToManyField(Model)`: Many-to-many.  
     - `OneToOneField(Model)`: One-to-one.  
   - **`on_delete` parameter**: Defines behavior when the related object is deleted (e.g., `CASCADE`, `SET_NULL`).

3. **Migrations**  
   - **Creating Migrations**:  
     ```bash
     python manage.py makemigrations
     ```
     This generates migration files in each app’s `migrations/` folder.  
   - **Applying Migrations**:  
     ```bash
     python manage.py migrate
     ```
     Executes or updates the database schema to match the models’ definitions.  
   - **Best Practice**: Migrations should be committed to version control so all environments stay in sync.

4. **Django ORM Basics**  
   - **Creating Objects**:  
     ```python
     obj = ModelName.objects.create(field1="value", field2=123)
     ```
   - **Retrieving**:  
     ```python
     results = ModelName.objects.filter(field1="value")
     single = ModelName.objects.get(id=1)
     ```
   - **Updating**: Either update fields on the instance and call `save()`, or use `update()` on a queryset.  
   - **Deleting**:  
     ```python
     obj.delete()
     ```
   - **Relationships**: Access related data with dot notation (e.g., `rental.bike` if you have a `ForeignKey` to `Bike`).

5. **Overriding the `save()` Method**  
   - **Purpose**: Insert custom logic before or after saving an object. For example, auto-calculating a fee or setting a default status.  
   - **Call `super().save(*args, **kwargs)`** to ensure the original save logic proceeds.  
   - **Caution**: Avoid overly complex logic in `save()` that might belong in signals or forms.

---

### **2. Step-by-Step Workshop**

Assume you have a **Django project** running in Docker Compose. Let’s add a new app for practice with models.

#### **Step 1: Create a New App**

1. **Command**  
   ```bash
   docker compose run web python manage.py startapp myapp
   ```
   - This generates a `myapp/` folder with `models.py`, `views.py`, etc.

2. **Add `myapp` to Installed Apps**  
   ```python
   INSTALLED_APPS = [
       # ...
       'myapp',
   ]
   ```
   in your `settings.py`.

#### **Step 2: Define Models in `myapp/models.py`**

1. **Example**  
   ```python
   from django.db import models

   class Bike(models.Model):
       name = models.CharField(max_length=200, unique=True)
       is_available = models.BooleanField(default=True)
       hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=50.00)

       def __str__(self):
           return self.name

   class Rental(models.Model):
       user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
       bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
       start_time = models.DateTimeField(auto_now_add=True)
       end_time = models.DateTimeField(blank=True, null=True)
       total_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

       def __str__(self):
           return f"{self.user} - {self.bike}"
   ```
2. **Override `save()`** (if needed)  
   ```python
   def save(self, *args, **kwargs):
       # e.g., calculate total_fee if end_time is set
       super().save(*args, **kwargs)
   ```

#### **Step 3: Migrations**

1. **Generate Migrations**  
   ```bash
   docker compose run web python manage.py makemigrations
   ```
   - You should see something like `Migrations for 'myapp': ...`.
2. **Apply Migrations**  
   ```bash
   docker compose run web python manage.py migrate
   ```
   - This updates the database schema.

#### **Step 4: Testing in the Django Shell**

1. **Shell**  
   ```bash
   docker compose run web python manage.py shell
   ```
2. **Create and Query**  
   ```python
   from myapp.models import Bike
   Bike.objects.create(name="Mountain Bike", hourly_rate=75.00)
   print(Bike.objects.all())
   ```
3. **Exit**  
   - Press `Ctrl+D` or type `exit()`.

#### **Step 5: Admin Registration (Optional)**

- If you want to manage these models in the admin:
  ```python
  # myapp/admin.py
  from django.contrib import admin
  from .models import Bike, Rental

  admin.site.register(Bike)
  admin.site.register(Rental)
  ```
- Create a superuser if you haven’t (`python manage.py createsuperuser`), then visit `http://localhost:8000/admin/`.

---

### **3. Assignment**

1. **Objective**  
   - Practice defining Django models, applying migrations, and performing basic CRUD operations via the ORM.

2. **Tasks**  
   1. **Add a `Book` Model**  
      - Fields: `title` (char), `author` (char), `published_date` (datetime), `price` (decimal).  
      - Override `__str__` to return a nice representation.  
   2. **Migrate**  
      - Run `makemigrations` and `migrate`.  
   3. **Shell Test**  
      - Insert a Book object and query it.  
      - Show your output from the Python shell.  

3. **Deliverables**  
   - **Code Snippet** of your `Book` model.  
   - **Screenshot** or copy-paste of your shell showing the created Book.  
   - Optional: Admin screenshot if you registered it.

---

### **4. Conclusion**

Django’s **models** provide a clean, high-level abstraction for database operations, freeing you from writing SQL for most tasks. By combining **fields**, **relationships**, and **migration** tools, you can evolve your schema over time while keeping data intact. This approach, coupled with Django’s shell for quick experimentation, streamlines building data-driven applications in containerized environments—where local changes can be tested and deployed confidently.
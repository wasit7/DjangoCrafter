# week04 Tutorial
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

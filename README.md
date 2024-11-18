```bash
django-admin startproject blog
python manage.py startapp api
python manage.py migrate
python manage.py runserver
```



```bash
docker build -t django-ninja-app .
docker run -p 8000:8000 django-ninja-app
```

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```


```python
from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Router

from .models import User

router = Router()


@router.get(path='/')
def get_users(request: HttpRequest) -> QuerySet[User]:
    users = User.objects.all()
    return users
```
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
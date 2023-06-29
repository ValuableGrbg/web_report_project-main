# Web repoter generator

## Commands to setup a connection with Postgresql:  
<br>

##### Commands in cmd:
- C:\Program Files\PostgreSQL\14\bin>psql -h 127.0.0.1 -U postgres -W
- CREATE DATABASE django_web_app WITH ENCODING='UTF-8' LC_CTYPE='en_US.UTF-8' LC_COLLATE='en_US.UTF-8' OWNER=postgres CONNECTION LIMIT=-1 template=template0;

##### Commands in python terminal (making migration of db):
- python manage.py migrate

##### Create django-app
- django-admin startapp analysis_app

##### Create superuser
- python manage.py createsuperuser
- dmitriy 0000

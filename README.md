# Mailing app

## Getting started

#### Copy the content from .env.example to .env file
```
cp .env.example .env
```

#### Then build containers with the following command

```
docker-compose up -d
```

#### Make and apply all the migrations.

```
python manage.py makemigrations
python manage.py migrate
```

Notice: you may have a problem with making migrations. If this is so, try to make them separatly for each app. Just like that:
```
python manage.py makemigrations project
python manage.py migrate project
```

#### Create a superuser to use Django-Admin panel.

```
cd backend/
python manage.py createsuperuser
```

#### Now, you are ready to use the API.
The project uses nginx, so it runs on 80 port (wtih default settings).
```
http://localhost/api/
```
#### Notice: you have to be authenticated to use the API, so use the:
```
http://localhost/auth/registration/
```
#### to create a user.
#### Then use this to authenticate:
```
http://localhost/auth/
```

#### If you want to see the API docs, then use
```
http://localhost/docs/
```

#### There is a script 'mailing.py' that runs every 15 minutes. It has logs at /logs/mailing.log

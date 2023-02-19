# EmailSystem

.env file

```
DEBUG=1
ENVIRONMENT_TYPE=development
SECRET_KEY=your_secret_kry
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=email_system
SQL_USER=postgres
SQL_PASSWORD=postgres
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
#celery
RABBITMQ_DEFAULT_USER=<user>
RABBITMQ_DEFAULT_PASS=<pwd>
CELERY_BROKER_URL=amqp://<user>:<password>@rabbit:5672
CELERY_SETTINGS_MODULE=emailsystem.settings
#email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER=<email>
EMAIL_HOST_PASSWORD=<pwd>
CORS_ORIGIN_ALLOW_ALL=1

```

- Install docker and docker-compose

- Keep the environment file .env.dev in project root directory

- run these commands in order:
```
docker-compose up -d --build
docker-compose exec web python manage.py migrate
```

- use this command to create superuser
```
docker-compose run web python manage.py createsuperuser
```

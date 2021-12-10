<h2> SPAM SEGREGATOR </h2>

## App Goal
> Download messages using IMAP <br>
> Analyze messages using Apache Spamassasin - https://spamassassin.apache.org/ 


## 🚀 Features

- Django 3.2 & Python 3.9
- Install via [Poetry](https://pypi.org/project/poetry/) and [Docker](https://www.docker.com/)
- User log in/out, sign up, password reset via [django-allauth](https://github.com/pennersr/django-allauth)
- Static files configured with [Whitenoise](http://whitenoise.evans.io/en/stable/index.html)
- Styling with [Bootstrap v4](https://github.com/twbs/bootstrap)
- DRY forms with [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms)
- Imap Client [imap-tools] (https://pypi.org/project/imap-tools/)
- Spamd Client [aiospamc] (https://pypi.org/project/aiospamc/)
- Task Managing [celery] (https://pypi.org/project/celery/)

----

## 📖 Installation
Spam Segregator can be installed via Docker. To start, clone the repo to your local computer and change into the proper directory.

```
$ git clone https://github.com/KubaTaba1uga/spam_segregator.git
$ cd spam_segregator
```

### Docker

```
$ docker-compose up -d
# Run Migrations
$ docker-compose exec web-app python manage.py migrate
# Create a Superuser
$ docker-compose exec web python manage.py createsuperuser
# Load the site at http://127.0.0.1:8000
```

For Docker, the `INTERNAL_IPS` configuration in `config/settings.py` must be updated to the following:

```python
# config/settings.py
# django-debug-toolbar
import socket
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]
```

## Setup

```
# Run Migrations
(djangox) $ python manage.py migrate

# Create a Superuser
(djangox) $ python manage.py createsuperuser

# Confirm everything is working:
(djangox) $ python manage.py runserver

# Load the site at http://127.0.0.1:8000
```

<!-- ## Docker Usage
```
# Build the Docker Image
$ docker-compose build

# Run Migrations
$ docker-compose run --rm web python manage.py migrate

# Create a Superuser
$ docker-compose run --rm web python manage.py createsuperuser

# Run Django on http://localhost:8000/
$ docker-compose up

# Run Django in background mode
$ docker-compose up -d

# Stop all running containers
$ docker-compose down

# Run Tests
$ docker-compose run --rm web pytest

# Re-build PIP requirements
$ docker-compose run --rm web pip-compile requirements/requirements.in
```-->



# App Description

I was curious, why Gmail/Exchange and other email providers, qualify messages as SPAM.

As AI/ML is not my scope of interests, I've decided to use Apache Spamassasin - https://spamassassin.apache.org/ for emails analysis, as it provides reports with explanation why message was qualified.

My month-work is small system which allows multiple users to analyze their mailboxes content concurrently.

I use some hacks over celery to make it happen and bypass IMAP limitations like, not allowing for simultaneous connections.

To allow for concurrent mailboxes analysis, workers are created dynamically for each user. Each user has its own worker and two queues. Queue for downloading messages, and queue for spam analysis.

To bypass IMAP simultaneous connections problem, each message is seperate task send to rabbitMQ, with retry policy and time delay. If connections collision is in place, system waits, and try again until the goal (downloading message) is accomplished.

By default workers are deleted, each 24h, if there are no pending/active tasks in their queues.

## App Usage Example

https://user-images.githubusercontent.com/73971628/146213891-c2f7e226-2e82-428e-ad74-c93e9f32bbab.mp4

## 🚀 Features

- Django 3.1 & Python 3.9
- Django Starter Template by [DjangoX](https://github.com/wsvincent/djangox)
- Install app with [Docker](https://www.docker.com/) and [Poetry](https://pypi.org/project/poetry/) 
- User log in/out, sign up, password reset via [django-allauth](https://github.com/pennersr/django-allauth)
- Static files configured with [Whitenoise](http://whitenoise.evans.io/en/stable/index.html)
- Styling with [Bootstrap v4](https://github.com/twbs/bootstrap)
- Debugging with [django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar)
- DRY forms with [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms)
- Database adapter by [psycopg2-binary](https://pypi.org/project/psycopg2-binary/)
- Database by [postgreSQL](https://www.postgresql.org/)
- Downloading emails with [imap-tools](https://pypi.org/project/imap-tools/)
- Analyze spam by [spamassasin](https://spamassassin.apache.org/)
- Analyze spam with [aiospamc](https://pypi.org/project/aiospamc/)
- Manage Tasks with [celery](https://pypi.org/project/celery/)
- Task Queue by [rabbitMQ](https://www.rabbitmq.com/)

----

## Table of Contents
* **[Installation](#installation)**
  * [Docker](#docker)
* [Setup](#setup)
* [Contributing](#contributing)
* [Support](#support)
* [License](#license)

----

## 📖 Installation
Spam Recycler can be installed via Docker.
```
$ git clone https://github.com/KubaTaba1uga/spam_recycler
$ cd spam_recycler
```

### Docker

```
$ docker-compose build 
$ docker-compose up -d
$ docker-compose exec web-app python manage.py migrate
$ docker-compose exec web-app python manage.py createsuperuser
# Load the site at http://127.0.0.1:8000
```

## License

[The MIT License](LICENSE)


## Docker Usage
```
# Build the Docker Image
$ docker-compose build

# Run Migrations
$ docker-compose run --rm web-app python manage.py migrate

# Create a Superuser
$ docker-compose run --rm web-app python manage.py createsuperuser

# Run Django on http://localhost:8000/
$ docker-compose up

# Run Django in background mode
$ docker-compose up -d

# Stop all running containers
$ docker-compose down

# Run Tests
$ docker-compose run --rm web-app pytest

```


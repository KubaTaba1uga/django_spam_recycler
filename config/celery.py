"""
Celery config file
https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html
"""
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# this code copied from manage.py
# set the default Django settings module for the 'celery' app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# you change change the name here
app = Celery("config")

# read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# load tasks.py in django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# create queue if is not exsisting
app.conf.task_create_missing_queues = True


from time import sleep


@app.task(bind=True)
def debug_task(self):
    sleep(10)
    print(f'DONE')

""" Start flower
        $  celery --broker=amqp://myuser:mypassword@localhost:5672/myvhost flower --port=5000
    Start worker
        $  celery -A config worker -l info

"""

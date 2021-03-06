"""
Celery config file
https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html
"""
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from datetime import timedelta
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

# create queues if they are not exsisting
app.conf.task_create_missing_queues = True

# Delete workers if they queues are empty
#  as each report should generate in less than 24 hours
#  we can delete workers in 24 hours period
#  This is not ideal solution, but it works
app.conf.beat_schedule = {'cleanup-workers': {
    'task': 'shared_code.worker_utils.delete_workers',
        'schedule': timedelta(hours=24),
}}

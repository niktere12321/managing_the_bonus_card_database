from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'managing.settings')

app = Celery("managing")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

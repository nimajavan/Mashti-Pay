from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pm.settings')
app = Celery('pm')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()




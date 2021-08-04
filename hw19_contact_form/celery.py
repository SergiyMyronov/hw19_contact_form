import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hw19_contact_form.settings')

app = Celery('hw19_contact_form')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

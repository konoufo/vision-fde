from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'D4.settings')

app = Celery('D4')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

'''
lister les tasks celery -A D4 worker -l info --pool=solo


python manage.py shell
from D4.tasks import add
add.delay(4,65)
add.apply_async((2,2), countdown=5)


'''
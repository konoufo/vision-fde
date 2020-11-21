from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
#https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html#django-first-steps


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'D4.settings')

app = Celery('D4')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

'''
lister les tasks celery -A D4 worker -l info --pool=solo


python manage.py shell
from D4.tasks import add
add.delay(4,65)
add.apply_async((2,2), countdown=5)


'''
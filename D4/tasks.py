from __future__ import absolute_import, unicode_literals
from celery import shared_task

@shared_task
def add(x, y):
    return x+y

''''


python manage.py shell
from D4.tasks import add
add.delay(4,65)
add.apply_async((2,2), countdown=5)


'''
import os

from celery import Celery
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inspire.settings')
app = Celery('main', broker=settings.CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send_mail_every_1_min': {
        'task': 'main.tasks.send_goodmorning',
        'schedule': 60,
    }
}

app.autodiscover_tasks()
# celery worker -A inspire -l info --pool=solo
# celery -A inspire beat -l info
# turn off celery -A inspire control shutdown

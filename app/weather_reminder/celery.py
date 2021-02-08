import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather_reminder.settings")

app = Celery("weather_reminder")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'update_cities_weather_info': {
        'task': 'core.tasks.update_cities_weather_data',
        'schedule': crontab(minute=50),
    },
}

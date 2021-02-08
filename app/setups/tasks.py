
from celery import shared_task

from .utils import send_email_with_weather_update


@shared_task(
    name="email_with_weather_update",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 5}
)
def email_with_weather_update(self, email):
    send_email_with_weather_update(email)

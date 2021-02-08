from celery import shared_task

from .utils.email_confirmation import send_confirmation_email
from .utils.update_cities_weather_forecast import update_cities_weather_forecats_from_api


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 5},
)
def confirmation_email(self, data):
    send_confirmation_email(data)

@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 5},
)
def update_cities_weather_data(self):
    update_cities_weather_forecats_from_api()

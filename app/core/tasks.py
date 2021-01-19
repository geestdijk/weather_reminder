from celery import shared_task

from .utils import send_confirmation_email


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 5},
)
def confirmation_email(self, data):
    send_confirmation_email(data)

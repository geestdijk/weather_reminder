from django.db.models.signals import post_save
from django.dispatch import receiver

from setups.enums import SetupStatus

from .models import Setup


@receiver(post_save, sender=Setup)
def create_or_update_scheduled_task(sender, instance, created, **kwargs):
    if created:
        instance.setup_task()
        instance.save()
    else:
        if instance.task is not None:
            instance.task.enabled = instance.status == SetupStatus.active
            instance.task.save()

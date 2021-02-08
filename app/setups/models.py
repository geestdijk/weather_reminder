import json

import pytz
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from django_enum_choices.fields import EnumChoiceField

from setups.enums import SetupStatus


class Setup(models.Model):

    class Meta:
        verbose_name = "Setup"

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    status = EnumChoiceField(SetupStatus, default=SetupStatus.active)
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(5, message="Should be at least 5"),
            MaxValueValidator(22, message="Should be at most 22"),
        ]
    )
    task = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, null=True, blank=True)

    def delete(self, *args, **kwargs):
        if self.task is not None:
            self.task.delete()

        return super().delete(*args, kwargs)

    def setup_task(self):
        self.task = PeriodicTask.objects.create(
            crontab=self.defined_time,
            name=f'Sending weather update via email for {self.user.email}',
            task='email_with_weather_update',
            args=json.dumps([self.user.email, ]),
        )

    @property
    def defined_time(self):
        if self.scheduled_time:
            defined_time, _ = CrontabSchedule.objects.get_or_create(
                minute='0',
                hour=f'{self.scheduled_time}',
                day_of_week='*',
                day_of_month='*',
                month_of_year='*',
                timezone=pytz.timezone("Europe/Kiev")
            )
            return defined_time

        raise NotImplementedError(
            f'''Interval Schedule for {self.scheduled_time} time is not added.'''
        )

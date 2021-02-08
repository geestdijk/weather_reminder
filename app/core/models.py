from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class City(models.Model):
    """City object"""

    name = models.CharField(max_length=255, unique=True)
    forecast = models.JSONField(default=list, blank=True, null=True)
    members = models.ManyToManyField(User, through="UserForecast")
    lat = models.DecimalField(max_digits=6, decimal_places=4, blank=True, null=True)
    long = models.DecimalField(max_digits=7, decimal_places=4, blank=True, null=True)

    def __str__(self):
        return self.name


class UserForecast(models.Model):
    """User Weather Forecast M2M object"""

    city = models.ForeignKey(City, related_name="cities", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="users", on_delete=models.CASCADE)

    def __str__(self):
        return f"City: {self.city.name}, User:{self.user.id}"

    class Meta:
        unique_together = ("city", "user")

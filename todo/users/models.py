from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    telegram_tag = models.CharField(max_length=50, blank=True)
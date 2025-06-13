from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    full_name = models.CharField("ФИО", max_length=150)
    address = models.CharField("Адрес", max_length=250)

    def __str__(self):
        return self.username
    

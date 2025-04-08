from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    username = models.CharField(max_length=30, unique=True)
    telefone = models.CharField(max_length=20, unique=True)
    nif = models.CharField(max_length=30, unique=True)

    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.username

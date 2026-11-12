from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('author', 'Автор'),
        ('admin', 'Админ')
    ]
    username = None
    email = models.EmailField(max_length=100, unique=True)
    role  = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email
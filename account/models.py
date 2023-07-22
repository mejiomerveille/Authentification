from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
import random


class User(AbstractUser):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=12, unique=True)
    is_phone_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=255)
    otp = models.CharField(max_length=6 , default="123456")


    def generate_otp(self):
        return str(random.randint(100000, 999999))

    def save(self, *args, **kwargs):
        if not self.id:
            self.otp = self.generate_otp()
        return super().save(*args, **kwargs)


    username = None

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = UserManager()
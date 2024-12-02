from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # 기본 AbstractUser 필드를 상속
    category= models.ManyToManyField('Category', blank=True)

class Category(models.Model):
    category = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category


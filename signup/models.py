

# class Interest(models.Model):
#     name = models.CharField(max_length=100, unique=True)  # 관심사 이름
#
#     def __str__(self):
#         return self.name
#
# class User(models.Model):
#     username = models.CharField(max_length=150, unique=True)
#     password = models.CharField(max_length=128)
#     email = models.EmailField(unique=True)
#     interests = models.ManyToManyField(Interest, blank=True)  # 다대다 관계 설정
#
#     def __str__(self):
#         return self.username

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # 기본 AbstractUser 필드를 상속하므로 추가 필드를 필요로 할 경우 정의합니다.
    interests = models.ManyToManyField('Interest', blank=True)

class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


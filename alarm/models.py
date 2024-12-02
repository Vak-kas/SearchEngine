from django.db import models
from signup.models import User
from main.models import Post



class NotificationSetting(models.Model):
    NOTIFICATION_CHOICES = [
        ('email', '이메일'),
        ('sms', 'SMS'),
        ('push', '푸시 알림'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_settings")
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_CHOICES)
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.notification_type}: {'활성화됨' if self.is_enabled else '비활성화됨'}"


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






class Alarm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="alarms")  # 알림 대상 사용자
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # 관련 게시글
    message = models.TextField()  # 알림 메시지
    is_read = models.BooleanField(default=False)  # 읽음 여부
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return f"Alarm for {self.user.username} - {self.post.title}"

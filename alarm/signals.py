from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import Post
from signup.models import User
from .models import NotificationSetting
from .observer import CategoryNotifier, EmailAlarm

@receiver(post_save, sender=Post)
def handle_post_save(sender, instance, created, **kwargs):
    if created:
        # 알림을 받을 사용자 필터링
        users = NotificationSetting.objects.filter(
            notification_type='email',
            is_enabled=True
        ).values_list('user', flat=True)

        if not users:
            return  # 알림을 받을 사용자가 없으면 종료

        # 알림 메시지 생성
        message = f"새로운 게시글이 등록되었습니다: {instance.title}"

        # 이메일 알림 발송
        notifier = CategoryNotifier()
        notifier.subscribe(EmailAlarm())
        notifier.notify_subscribers(users, instance, message)

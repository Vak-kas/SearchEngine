from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import Final
from signup.models import User, Category
from .models import NotificationSetting
from .observer import CategoryNotifier, LoggingAlarm


@receiver(post_save, sender=Final)
def handle_final_save(sender, instance, created, **kwargs):
    if created:
        print(f"Signal triggered for Final: {instance.id}, created: {created}")

        # Category 객체 조회
        try:
            category_obj = Category.objects.get(category=instance.category)
            print(f"Category object found: {category_obj}")
        except Category.DoesNotExist:
            print(f"Category '{instance.category}' does not exist in the database.")
            return


        users = User.objects.filter(
            category=category_obj,
            notification_settings__notification_type='push',
            notification_settings__is_enabled=True
        )

        print(f"Users found for category '{instance.category}': {[user.username for user in users]}")

        if not users.exists():
            print(f"No users found for category: {instance.category}")
            return

        # 알림 메시지 생성
        message = f"새로운 게시글이 등록되었습니다: {instance.post.title}"

        # LoggingAlarm 사용
        notifier = CategoryNotifier()
        notifier.subscribe(LoggingAlarm())
        notifier.notify_subscribers(users, instance.post, message)
        print(f"Notification sent for Final: {instance.category}")



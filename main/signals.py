from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .classify import process_post_to_final

@receiver(post_save, sender=Post)
def handle_post_save(sender, instance, created, **kwargs):
    if created:
        # 새로 저장된 Post를 Final로 처리
        process_post_to_final(instance.id)

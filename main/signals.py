from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .classify import *

@receiver(post_save, sender=Post)
def handle_post_save(sender, instance, created, **kwargs):
    if created:
        # OpenAI 전략 사용
        strategy = BackendStrategy()
        process_post_to_final(instance.id, strategy)

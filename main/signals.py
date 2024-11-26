from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .classify import process_post_to_final

@receiver(post_save, sender=Post)
def handle_post_save(sender, instance, created, **kwargs):
    if created:
        process_post_to_final(instance.id)

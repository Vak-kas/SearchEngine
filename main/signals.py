from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Final
from .classifyCategory import BackendCategory, process_post_to_final
from .classifyTags import OpenAITags, MostWord, process_tags


@receiver(post_save, sender=Post)
def handle_post_save(sender, instance, created, **kwargs):
    if created:
        try:
            # 카테고리 처리
            category_strategy = BackendCategory()
            process_post_to_final(instance.id, category_strategy)

            # 태그 처리
            process_tags(instance.id)  # 전략은 process_tags 내부에서 처리
            print(f"Post ID {instance.id}: 카테고리와 태그 처리가 완료되었습니다.")
        except Exception as e:
            print(f"Error processing Post ID {instance.id}: {e}")


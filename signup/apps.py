from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class SignupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'signup'

    def ready(self):
        # post_migrate 신호 등록
        from .models import Category
        @receiver(post_migrate, sender=self)
        def create_default_categories(sender, **kwargs):
            category_list = ['네트워크', '보안', '프론트', '백엔드', 'AI', '게임', 'ios', '안드로이드']
            for name in category_list:
                Category.objects.get_or_create(category=name)

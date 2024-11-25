from django.apps import AppConfig


class SignupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'signup'

    def ready(self):
        from .models import Interest

        interest_names = ['네트워크', '보안', '프론트', '백엔드', 'AI', '게임', 'ios', '안드로이드']

        for name in interest_names:
            Interest.objects.get_or_create(name=name)

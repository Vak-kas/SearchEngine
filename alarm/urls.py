from django.urls import path
from .views import notification_settings

urlpatterns = [
    path('notification-settings/', notification_settings, name='notification-settings'),
]

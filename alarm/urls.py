from django.urls import path
from .views import notification_settings, mark_alarm_read
from .views import index

urlpatterns = [
    path('notification-settings/', notification_settings, name='notification-settings'),
    path('mark-read/<int:alarm_id>/', mark_alarm_read, name='mark_alarm_read'),
    path('', index, name='main'),  # 이 라인이 정확히 설정되었는지 확인
]

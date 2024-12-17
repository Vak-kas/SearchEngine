from django.contrib import admin
from .models import NotificationSetting
from django.contrib import admin
from .models import Alarm
@admin.register(NotificationSetting)
class NotificationSettingAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'is_enabled')
    search_fields = ('user__username', 'notification_type')
    list_filter = ('is_enabled', 'notification_type')



@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')

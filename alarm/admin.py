from django.contrib import admin
from .models import NotificationSetting

@admin.register(NotificationSetting)
class NotificationSettingAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'is_enabled')
    search_fields = ('user__username', 'notification_type')
    list_filter = ('is_enabled', 'notification_type')

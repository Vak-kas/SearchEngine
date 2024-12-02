from django import forms
from .models import NotificationSetting

class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = NotificationSetting
        fields = ['notification_type', 'is_enabled']

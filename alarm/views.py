from django.shortcuts import render, redirect
from .forms import NotificationSettingsForm
from .models import NotificationSetting
from django.shortcuts import render
from alarm.models import Alarm
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden
import logging
logger = logging.getLogger(__name__)

from alarm.models import Alarm

def index(request):
    if not request.user.is_authenticated:
        print("User is not authenticated.")
        return redirect('login')

    try:
        print(f"Request User: {request.user}")
        unread_alarms = Alarm.objects.filter(user=request.user, is_read=False)
        print(f"Unread alarms queryset: {unread_alarms}")
        logger.info(f"Unread alarms: {[alarm.message for alarm in unread_alarms]}")


        for alarm in unread_alarms:
            print(f"Alarm: {alarm.message} - Created At: {alarm.created_at}")

    except Exception as e:
        print(f"Error in fetching alarms: {e}")
        unread_alarms = []

    return render(request, 'main/main.html', {
        'unread_alarms': unread_alarms,
    })






def mark_alarm_read(request, alarm_id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    alarm = get_object_or_404(Alarm, id=alarm_id, user=request.user)
    alarm.is_read = True
    alarm.save()
    return redirect('main')


def notification_settings(request):
    if not request.user.is_authenticated:
        return redirect('login')  # 로그인하지 않은 사용자 리디렉션

    if request.method == 'POST':
        form = NotificationSettingsForm(request.POST)
        if form.is_valid():
            # 알림 설정 저장
            notification_setting, created = NotificationSetting.objects.get_or_create(
                user=request.user,
                notification_type=form.cleaned_data['notification_type']
            )
            notification_setting.is_enabled = form.cleaned_data['is_enabled']
            notification_setting.save()


            return redirect('main')
    else:
        settings = NotificationSetting.objects.filter(user=request.user)
        form = NotificationSettingsForm()

    return render(request, 'alarm/notification_settings.html', {
        'settings': settings,
        'form': form
    })

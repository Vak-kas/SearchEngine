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
        logger.warning("Unauthenticated user attempted to access the main page.")
        return redirect('login')

    try:
        logger.info(f"Fetching alarms for user: {request.user}")
        # 'push' 알림이 활성화된 사용자만 알림 표시
        push_enabled = NotificationSetting.objects.filter(
            user=request.user, notification_type='push', is_enabled=True
        ).exists()

        unread_alarms = []
        if push_enabled:
            unread_alarms = Alarm.objects.filter(user=request.user, is_read=False)

        logger.info(f"Unread alarms: {[alarm.message for alarm in unread_alarms]}")
    except Exception as e:
        logger.error(f"Error fetching alarms: {e}")
        unread_alarms = []

    return render(request, 'main/main.html', {
        'unread_alarms': unread_alarms,
    })





# def mark_alarm_read(request, alarm_id):
#     if not request.user.is_authenticated:
#         return HttpResponseForbidden()
#
#     alarm = get_object_or_404(Alarm, id=alarm_id, user=request.user)
#     alarm.is_read = True
#     alarm.save()
#     return redirect('main')
def mark_alarm_read(request, alarm_id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    alarm = get_object_or_404(Alarm, id=alarm_id, user=request.user)
    alarm.is_read = True
    alarm.save()
    logger.info(f"Alarm {alarm_id} marked as read for user {request.user}.")

    # next 파라미터로 전달된 URL로 리디렉션
    next_url = request.GET.get('next', 'main')  # 'next'가 없으면 메인으로 이동
    return redirect(next_url)

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

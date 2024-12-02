from django.shortcuts import render, redirect
from .forms import NotificationSettingsForm
from .models import NotificationSetting

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

            # 설정 저장 후 메인 페이지로 리디렉션
            return redirect('main')
    else:
        # 사용자의 기존 알림 설정 가져오기
        settings = NotificationSetting.objects.filter(user=request.user)
        form = NotificationSettingsForm()

    return render(request, 'alarm/notification_settings.html', {
        'settings': settings,
        'form': form
    })

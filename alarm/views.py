from django.shortcuts import render, redirect
from .forms import NotificationSettingsForm
from .models import NotificationSetting
from django.shortcuts import render
from alarm.models import Alarm
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden
from signup.models import UserTagHistory
from main.models import Tags, Post
from django.db.models import Count
import logging
logger = logging.getLogger(__name__)


from alarm.models import Alarm


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # 알림 설정 확인: push 알림이 활성화된 경우만 처리
    push_enabled = NotificationSetting.objects.filter(user=request.user, notification_type='push', is_enabled=True).exists()

    # 읽지 않은 알림 가져오기 (push 알림 설정이 켜져 있을 때만)
    if push_enabled:
        unread_alarms = Alarm.objects.filter(user=request.user, is_read=False)
    else:
        unread_alarms = []  # push 알림이 비활성화된 경우 알림 없음

    # 사용자 태그 기록 조회
    user_tags = UserTagHistory.objects.filter(user=request.user)
    tag_weights = {tag.tag: tag.count for tag in user_tags}

    # 관련 게시글 검색
    posts = Post.objects.filter(final__tags__tag__in=tag_weights.keys()).distinct()

    # 점수 계산: 태그 가중치를 기반으로 게시글 추천 점수 계산
    post_scores = {}
    for post in posts:
        tags = Tags.objects.filter(final__post=post)
        score = sum(tag_weights.get(tag.tag, 0) for tag in tags)
        post_scores[post] = score

    # 추천 순으로 정렬
    recommended_posts = sorted(post_scores.keys(), key=lambda x: post_scores[x], reverse=True)[:5]

    return render(request, 'main/main.html', {
        'unread_alarms': unread_alarms,
        'recommended_posts': recommended_posts,
    })




def mark_alarm_read(request, alarm_id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    alarm = get_object_or_404(Alarm, id=alarm_id, user=request.user)
    alarm.is_read = True
    alarm.save()

    # 태그 기록 업데이트
    tags = Tags.objects.filter(final__post=alarm.post)
    for tag in tags:
        tag_history, created = UserTagHistory.objects.get_or_create(user=request.user, tag=tag.tag)
        if not created:
            tag_history.count += 1
            tag_history.save()

    logger.info(f"Alarm {alarm_id} marked as read for user {request.user}.")
    next_url = request.GET.get('next', 'main')
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


from collections import Counter

def recommend_posts(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    # 사용자 태그 기록 조회
    user_tags = UserTagHistory.objects.filter(user=request.user)
    tag_weights = {tag.tag: tag.count for tag in user_tags}

    # 관련 게시글 검색
    posts = Post.objects.filter(final__tags__tag__in=tag_weights.keys()).distinct()

    # 점수 계산: 태그 가중치를 기반으로 게시글 추천 점수 계산
    post_scores = {}
    for post in posts:
        tags = Tags.objects.filter(final__post=post)
        score = sum(tag_weights.get(tag.tag, 0) for tag in tags)
        post_scores[post] = score

    # 추천 순으로 정렬
    recommended_posts = sorted(post_scores.keys(), key=lambda x: post_scores[x], reverse=True)

    return render(request, 'main/recommendations.html', {
        'recommended_posts': recommended_posts
    })

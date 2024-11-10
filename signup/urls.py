from django.urls import path
from .views import signup_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),  # '/signup/' 경로를 signup_view와 연결
]

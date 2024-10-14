from django.urls import path

from search import views

urlpatterns = [
    path('', views.index),
    path('search/', views.search_view),
]
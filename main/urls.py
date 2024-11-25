from django.urls import path
from .views import *

urlpatterns = [
    path('collect/', collect_and_save)
]

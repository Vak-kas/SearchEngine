from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='main'),
    path('collect/', collect_and_save, name = 'collect'),
]

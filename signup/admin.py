from django.contrib import admin
from .models import User, Interest

# User 모델 등록
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')

# Interest 모델 등록
@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

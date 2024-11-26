from django.contrib import admin
from .models import User, Category

# User 모델 등록
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')

# Interest 모델 등록
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    search_fields = ('category',)


class CategoryInline(admin.TabularInline):
    model = User.category.through
    extra = 1
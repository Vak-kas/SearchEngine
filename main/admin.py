from django.contrib import admin
from .models import Post, Final

# Post 모델 등록
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'title', 'author', 'content')  # 표시할 필드 설정
    search_fields = ('title', 'author', 'url')  # 검색 가능 필드
    list_filter = ('author',)  # 필터 추가

# Final 모델 등록
@admin.register(Final)
class FinalAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'category')  # 표시할 필드 설정
    search_fields = ('category',)  # 검색 가능 필드
    list_filter = ('category',)  # 필터 추가

from django.contrib import admin
from .models import ScrapedPost

@admin.register(ScrapedPost)
class ScrapedPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'host', 'author', 'interest', 'write_at')
    search_fields = ('title', 'author', 'tags')
    list_filter = ('host', 'interest')

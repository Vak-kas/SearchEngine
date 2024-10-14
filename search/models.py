from django.db import models

# Create your models here.
class Urls(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    tags = models.JSONField()
    summary = models.TextField(blank=True, null=True)
    content_html = models.TextField()
    write_at = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


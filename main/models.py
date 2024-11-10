from django.db import models

class ScrapedPost(models.Model):
    HOST_CHOICES = [
        ('velog', 'Velog'),
        ('tistory', 'Tistory'),
        ('naver', 'Naver'),
    ]

    host = models.CharField(max_length=50, choices=HOST_CHOICES)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    url = models.URLField(unique=True)
    tags = models.TextField()  # 여러 태그를 쉼표로 구분하여 저장
    interest = models.CharField(max_length=50)
    write_at = models.CharField(max_length=50)  # 날짜 형식에 따라 CharField 또는 DateField 사용 가능

    def __str__(self):
        return f"{self.title} ({self.host})"

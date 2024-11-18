from django.db import models

class Post(models.Model):

    host = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    url = models.URLField(unique=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.title} ({self.host})"


class Final(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='final')
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.post.url} - {self.category}"
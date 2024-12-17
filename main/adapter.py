from .models import Post
from django.http import JsonResponse
from urllib.parse import urlparse
from abc import ABC, abstractmethod
import logging
logger = logging.getLogger(__name__)



# Adapter 인터페이스
class Adapter(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def transform_and_save(self):
        pass




class SoloAdapter(Adapter):
    def transform_and_save(self):
        if not self.data.get('url') or not self.data.get('content'):
            return JsonResponse({'error': 'url과 content가 없음'}, status=400)

        # Post 객체 생성
        post = Post(
            url=self.data['url'],
            content=self.data['content'],
            host=get_host(self.data['url']),
            title=self.data.get('title', None),
            author=self.data.get('author', None)
        )

        try:
            post.save()
            return JsonResponse({'message': '저장 완료'}, status=201)
        except Exception as e:
            logger.error(f"Failed to save post: {self.data['url']}, Error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

class ScrapyAdapter(Adapter):
    def transform_and_save(self):
        pass


def get_host(url):
    try:
        host = urlparse(url)
        return host.netloc
    except Exception as e:
        raise ValueError(f"Invalid URL: {e}")


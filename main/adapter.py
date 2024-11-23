from .models import Post
from django.http import JsonResponse



class PostAdapter:
    def __init__(self, data):
        self.data = data

    def transform_and_save(self):
        if not self.data.get('url') or not self.data.get('content'):
            return JsonResponse({'error': 'url과 content가 없음'}, status=400)

        # Post 객체 생성
        post = Post(
            url=self.data['url'],
            content=self.data['content'],
            host=self.data.get('host', None), #업데이트 예정, url에서 뽑아오는 걸로 수정 예정
            title=self.data.get('title', None),
            author=self.data.get('author', None)
        )

        try:
            post.save()
            return JsonResponse({'message': '저장 완료'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



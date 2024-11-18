from .models import Post
from django.http import JsonResponse



class PostAdapter:
    def __init__(self, data):
        self.data = data

    def transform_and_save(self):
        # 필수 필드인 url과 content가 있는지 확인
        if not self.data.get('url') or not self.data.get('content'):
            return JsonResponse({'error': 'url과 content는 필수입니다.'}, status=400)

        # Post 객체 생성
        post = Post(
            url=self.data['url'],
            content=self.data['content'],
            host=self.data.get('host'),  # 만약 없다면 모델의 save 메서드에서 처리됨
            title=self.data.get('title', None),
            author=self.data.get('author', None)
        )

        try:
            post.save()  # 모델의 save 메서드에서 host가 비어있으면 url에서 추출
            return JsonResponse({'message': 'Post가 성공적으로 저장되었습니다.'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



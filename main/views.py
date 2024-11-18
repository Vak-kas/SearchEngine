from django.http import JsonResponse
from .factory import CollectorFactory
from .adapter import PostAdapter

def collect_and_save(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=405)

    collector_type = request.POST.get('collector_type')
    url = request.POST.get('url')

    if not collector_type or not url:
        return JsonResponse({'error': 'collector_type과 url은 필수입니다.'}, status=400)

    try:
        # 팩토리 패턴을 사용하여 수집기 생성
        collector = CollectorFactory.create_collector(collector_type)
        data = collector.collect_data(url)

        if data:
            # PostAdapter를 사용하여 데이터를 저장
            adapter = PostAdapter(data)
            response = adapter.transform_and_save()
            return response
        else:
            return JsonResponse({'error': '데이터 수집에 실패했습니다.'}, status=500)

    except ValueError as ve:
        return JsonResponse({'error': str(ve)}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'알 수 없는 오류가 발생했습니다: {e}'}, status=500)

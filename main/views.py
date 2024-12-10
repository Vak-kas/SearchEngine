from .adapter import Adapter, SoloAdapter
from .forms import CollectorForm
from django.http import JsonResponse
from .factory import CollectorFactory
from django.shortcuts import render, redirect



def index(request):
    return redirect('main')




def collect_and_save(request):
    if request.method == 'POST':
        # URL 데이터 가져오기
        url = request.POST.get('url')
        collector_type = request.POST.get('collector_type')  # 'scrapy', 'selenium', 'solo'

        if not url or not collector_type:
            return JsonResponse({'error': 'URL 또는 수집기 유형이 제공되지 않았습니다.'}, status=400)

        try:
            collector = CollectorFactory.create_collector(collector_type)
            collected_data = collector.collect_data(url)
            print(collected_data)

            if not collected_data:
                return JsonResponse({'error': f'{collector_type} 수집기: 데이터 수집 실패'}, status=500)

            return redirect('main')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'GET':
        form = CollectorForm()
        return render(request, 'main/collector_form.html', {'form': form})

    return JsonResponse({'error': 'POST 요청만 지원됩니다.'}, status=405)




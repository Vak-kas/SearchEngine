import os
import sys
from django.shortcuts import render
from .forms import SearchForm
from .models import Urls
from django.http import HttpResponse

# Scrapy 프로젝트 경로 추가
# sys.path.append('/Users/seo/Desktop/github/codering/scrapy/velog_scrapy')
# os.environ['SCRAPY_SETTINGS_MODULE'] = 'velog_scrapy.settings'


def index(request):
    return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")


# 스크래피 실행 함수
def run_spider(search_term):
    # 현재 작업 디렉토리를 Scrapy 프로젝트 디렉토리로 설정
    os.chdir('search/velog_scrapy')

    # Scrapy 명령어 실행
    os.system(f'scrapy crawl velog -a search_term={search_term}')


def search_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']

            # Scrapy 크롤러 실행
            run_spider(search_term)

            # 크롤링된 데이터 가져오기
            posts = Urls.objects.all()
            print(posts)
            return render(request, 'scrapy/scraped_data.html', {'posts': posts})
    else:
        form = SearchForm()
    return render(request, 'scrapy/search.html', {'form': form})

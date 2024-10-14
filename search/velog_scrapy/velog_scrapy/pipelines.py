# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import django
import sys



sys.path.append('/Users/seo/Desktop/github/codering')  # Django 프로젝트 루트 경로
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Django settings 경로
django.setup()
from search.models import Urls
from asgiref.sync import sync_to_async
class VelogScrapyPipeline:
    @sync_to_async
    def process_item(self, item, spider):

        url = Urls.objects.create(
            url=item['url'],
            title=item['title'],
            tags=item['tags'],
            summary='',  # 이 부분도 빈 값으로 저장
            content_html=item['content_html']
        )
        url.save()
        return item




from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from main.adapter import SoloAdapter, ScrapyAdapter


# 수집기 인터페이스
class Collector(ABC):
    @abstractmethod
    def collect_data(self, url, adapter):
        pass


# A형 수집기 예시 (웹 스크래핑)
class ScrapyCollector(Collector):
    def __init__(self, adapter):
        self.adapter = adapter

    def collect_data(self, url):
        # data = {
        #     'url': url,
        #     'content': 'Scrapy로 수집된 콘텐츠',
        #     'title': 'Scrapy 제목',
        #     'author': 'Scrapy 작가'
        # }
        # return self.adapter.transform_and_save(data)
        pass


# B형 수집기 예시 (API 호출)
class SeleniumCollector(Collector):
    def __init__(self):
        pass

    def collect_data(self, url):
        # Selenium 데이터 수집 로직 구현
        print("Selenium 데이터 수집 로직 실행")
        return None


# SoloCollector 정의
class SoloCollector(Collector):
    def __init__(self, adapter):
        self.adapter = adapter

    def collect_data(self, url):
        if not url:
            raise ValueError("URL이 없음")

        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.title.string if soup.title else None
            # content = soup.get_text()
            content = response.text
            data = {
                'url': url,
                'content': content.strip(),
                'host': None,  # host는 Adapter에서 처리 예정
                'title': title,
                'author': None
            }
            self.adapter.data = data
            return self.adapter.transform_and_save()
        except Exception as e:
            print(f"Error collecting data from {url}: {e}")
            return None



# CollectorFactory 구현
class CollectorFactory:
    @staticmethod
    def create_collector(collector_type):
        """
        필요한 Collector와 Adapter를 연결하여 생성
        """
        if collector_type == 'scrapy':
            adapter = ScrapyAdapter()
            return ScrapyCollector(adapter=adapter)
        elif collector_type == 'selenium':
            return SeleniumCollector()  # Selenium은 Adapter 구현이 필요 없음
        elif collector_type == 'solo':
            adapter = SoloAdapter({})
            return SoloCollector(adapter=adapter)
        else:
            raise ValueError("지원하지 않는 수집기 유형입니다.")

from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from .views import PostAdapter
# 수집기 인터페이스
class Collector(ABC):
    @abstractmethod
    def collect_data(self):
        pass

# A형 수집기 예시 (웹 스크래핑)
class ScrapyCollector(Collector):
    def collect_data(self):
        # 실제 스크래핑 로직을 여기에 구현
        return {
            'url': 'https://example.com',
            'content': 'This is example content.',
            'host': None,  # 호스트는 어댑터에서 처리
            'title': 'Example Title',
            'author': 'Author Name'
        }

# B형 수집기 예시 (API 호출)
class SeleniumCollector(Collector):
    def collect_data(self):
        # 실제 API 호출 로직을 여기에 구현
        return {
            'url': 'https://api.example.com/data',
            'content': 'This is content from API.',
            'host': 'api.example.com',
            'title': 'API Data Title',
            'author': 'API Author'
        }


class SoloCollector(Collector):
    def collect_data(self, url):
        if not url:
            raise ValueError("URL이 없음")

        try:
            # URL로 HTTP GET 요청
            response = requests.get(url)
            response.raise_for_status()  # 상태 코드 확인

            # BeautifulSoup을 사용하여 HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')

            # 기본 데이터 수집 (예: 타이틀 및 본문)
            title = soup.title.string if soup.title else None
            content = soup.get_text()

            # 수집된 데이터를 반환
            return {
                'url': url,
                'content': content.strip(),
                'host': None,  # host는 PostAdapter에서 처리 예정
                'title': title,
                'author': None  # 특별한 로직으로 채우지 않음
            }
        except Exception as e:
            print(f"Error collecting data from {url}: {e}")
            return None


# CollectorFactory 구현
class CollectorFactory:
    @staticmethod
    def create_collector(collector_type):
        if collector_type == 'scrapy':
            return ScrapyCollector()
        elif collector_type == 'selenium':
            return SeleniumCollector()
        elif collector_type == 'solo':
            return SoloCollector()
        else:
            raise ValueError("지원하지 않는 수집기 유형입니다.")


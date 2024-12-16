from decouple import config
from abc import ABC, abstractmethod

from django.db import transaction

from .models import Post, Final, Tags
from signup.models import Category
from openai import OpenAI
from django.conf import settings
import logging

from collections import Counter
import re



logger = logging.getLogger(__name__)

client = OpenAI(
    api_key = config("OPENAI_API_KEY", default="")
)

class TagsStrategy(ABC):
    @abstractmethod
    def analyze_tags(self, content, categories):
        pass


#ChatGPT API
class OpenAITags(TagsStrategy):
    def analyze_tags(self, content, categories):
        messages = [
            {
                "role": "system",
                "content": (
                    "그리고 주어지는 웹사이트의 url의 콘텐트는 다음과 같다."
                    "사용자가 제공한 콘텐츠를 분석하여 이 목록에서 가장 적합한 태그들 10개 이내로 출력해줘.\n"
                    "한 단어씩 ,를 기준으로 태그 생성해줘. 추가적인 부연설명은 필요 없어."
                )
            },
            {
                "role": "user",
                "content": f"이 콘텐츠의 태그가 될만한 단어 10개 이내로 ','를 기준으로 대답해줘. \n\n{content}"
            }
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        result_category = response.choices[0].message.content.strip()
        return result_category



class MostWord(TagsStrategy):
    def analyze_tags(self, content, categories):
        words = re.findall(r'\b\w+\b', content.lower())

        word_counts = Counter(words)

        # 가장 많이 등장한 단어 상위 10개 추출
        most_common_words = [word for word, count in word_counts.most_common(10)]


        # 태그 문자열로 변환
        tags = ','.join(most_common_words)
        print(tags)

        return tags


class Similar(TagsStrategy):
    def analyze_tags(self, content, categories):
        pass

def process_tags(post_id, strategies=None):
    try:
        post = Post.objects.get(id=post_id)
        content = post.content

        final, created = Final.objects.get_or_create(post=post)

        # 전략 기본값 설정
        if strategies is None:
            strategies = [OpenAITags(), MostWord()]

        # 모든 전략 실행 및 태그 수집
        all_tags = set()
        for strategy in strategies:
            tags_string = strategy.analyze_tags(content, None)
            tags_list = [tag.strip() for tag in tags_string.split(",") if tag.strip()]
            all_tags.update(tags_list)

        # Tags 모델에 태그 저장 (트랜잭션 처리)
        with transaction.atomic():
            # 기존 태그 삭제
            Tags.objects.filter(final=final).delete()

            # 새 태그 저장
            for tag in all_tags:
                Tags.objects.create(final=final, tag=tag)

        print(f"Tags saved successfully for Post ID {post_id}: {all_tags}")

    except Exception as e:
        print(f"Error processing tags for Post ID {post_id}: {e}")





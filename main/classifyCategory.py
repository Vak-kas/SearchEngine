from decouple import config
from abc import ABC, abstractmethod
from .models import Post, Final
from signup.models import Category
from openai import OpenAI
from django.conf import settings
import logging


logger = logging.getLogger(__name__)

client = OpenAI(
    api_key = config("OPENAI_API_KEY", default="")
)

class CategoryStrategy(ABC):
    @abstractmethod
    def analyze_category(self, content, categories):
        pass


#ChatGPT API
class OpenAICategory(CategoryStrategy):
    def analyze_category(self, content, categories):
        messages = [
            {
                "role": "system",
                "content": (
                    f"카테고리 목록이 다음과 같이 주어진다. : {', '.join(categories)}.\n"
                    "그리고 주어지는 웹사이트의 url의 콘텐트는 다음과 같다."
                    "사용자가 제공한 콘텐츠를 분석하여 이 목록에서 가장 적합한 카테고리 단어를 하나만 선택해라.\n"
                    "반드시 카테고리 단어 중 하나만 말해라. 추가적인 부연설명은 필요 없어."
                )
            },
            {
                "role": "user",
                "content": f"이 콘텐츠는 어떤 카테고리에 속하는가??\n\n{content}"
            }
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        result_category = response.choices[0].message.content.strip()
        return result_category

#무조건 백엔드
class BackendCategory(CategoryStrategy):
    def analyze_category(self, cont, categories):
        result_category = "백엔드"
        return result_category



def process_post_to_final(post_id, strategy):
    try:
        post = Post.objects.get(id=post_id)
        content = post.content

        categories = list(Category.objects.values_list('category', flat=True))
        if not categories:
            logger.error("No categories available in the database.")
            return

        result_category = strategy.analyze_category(content, categories)

        final_entry, created = Final.objects.get_or_create(
            post=post,
            defaults={'category': result_category}
        )

        if created:
            logger.info(f"Category '{result_category}' saved successfully for Post ID: {post_id}.")
        else:
            logger.info(f"Post ID {post_id} already exists in Final. Category: '{final_entry.category}'.")

    except Post.DoesNotExist:
        logger.error(f"Post with ID {post_id} does not exist.")
    except Exception as e:
        logger.error(f"Error processing Post ID {post_id}: {e}")

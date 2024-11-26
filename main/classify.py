from decouple import config
from openai import OpenAI
from .models import Post, Final
from signup.models import Category
import logging
logger = logging.getLogger(__name__)



client = OpenAI(
    api_key = config("OPENAI_API_KEY", default="")
)

def process_post_to_final(post_id):
    try:
        # Post 데이터 가져오기
        post = Post.objects.get(id=post_id)
        content = post.content
        url = post.url

        # Category 모델에서 카테고리 목록 가져오기
        categories = list(Category.objects.values_list('category', flat=True))

        if not categories:
            return "No categories available in the database."

        # OpenAI API 메시지 구성
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

        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        # 결과 카테고리 추출
        print(response.choices[0].message)
        result_category = response.choices[0].message.content.strip()

        # Final 모델에 데이터 저장
        final_entry, created = Final.objects.get_or_create(
            post=post,  # post 객체 사용
            defaults={'category': result_category}
        )

        if created:
            logger.info(f"Category '{result_category}' saved successfully for URL: {url}.")
        else:
            logger.info(f"URL already exists in Final. Category: '{final_entry.category}'.")
    except Exception as e:
        logger.error(f"Error processing Post ID {post_id}: {e}")

    except Post.DoesNotExist:
        return f"Post with ID {post_id} does not exist."
    except Exception as e:
        return f"Error: {e}"

import scrapy
from ..items import VelogScrapyItem

class VelogSpider(scrapy.Spider):
    name = "velog"
    allowed_domains = ["velog.io"]
    start_urls = ["https://velog.io?search?q="]


    def __init__(self, search_term=None, *args, **kwargs):
        super(VelogSpider, self).__init__(*args, **kwargs)
        if search_term:
            self.start_urls = [f'https://velog.io/search?q={search_term}']

    def parse(self, response):
        posts = response.xpath('//*[@id="root"]/div[2]/div[3]/div[2]/div')
        for post in posts[:10]:
            item = VelogScrapyItem()
            item['title'] = post.xpath('.//h2/text()').get()  # 제목 가져오기
            item['url'] = response.urljoin(post.xpath('.//a/@href').get())  # 제목에 해당하는 URL 가져오기
            item['tags'] = post.xpath('.//ul[@class="tags"]/a/text()').getall()  # 태그들 가져오기
            item['summary'] = ""
            item['content_html'] = ""
            item['write_at'] = post.xpath('.//div[contains(@class, "subinfo")]/span/text()').get()
            yield item

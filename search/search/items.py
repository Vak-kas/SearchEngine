# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
class VelogScrapyItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()
    summary = scrapy.Field()
    content_html = scrapy.Field()
    write_at = scrapy.Field()
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YandexItem(scrapy.Item):
    domain = scrapy.Field()
    title = scrapy.Field()
    probable_name = scrapy.Field()
    place_in_search = scrapy.Field()

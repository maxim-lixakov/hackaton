# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DomainItem(scrapy.Item):
    domain = scrapy.Field()
    title = scrapy.Field()
    probable_name = scrapy.Field()
    place_in_search_yandex = scrapy.Field()
    place_in_search_google = scrapy.Field()

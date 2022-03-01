# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class EgrulItem(Item):
    domain = Field()
    inn = Field()
    place_in_search_yandex = Field()
    place_in_search_google = Field()
    title = Field()
    probable_name = Field()
    full_name = Field()
    ogrn = Field()
    director = Field()
    domain_company_inn_match = Field()

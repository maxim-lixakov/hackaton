# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class DomainItem(scrapy.Item):
    domain = scrapy.Field()
    title = scrapy.Field()
    probable_name = scrapy.Field()
    place_in_search_yandex = scrapy.Field()
    place_in_search_google = scrapy.Field()
    commercial_search = scrapy.Field()
    details_num = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()

class CompanyInfoItem(scrapy.Item):
    domain = Field()
    inn = Field()
    place_in_search_yandex = Field()
    place_in_search_google = Field()
    authorized_capital = Field()
    grade = Field()
    title = Field()
    probable_name = Field()
    date_reg = Field()
    ogrn = Field()
    name = Field()
    director = Field()
    activity = Field()
    fines = Field()
    planned_checks = Field()
    unplanned_checks = Field()
    infringement = Field()
    not_infringement = Field()
    unknown_infringement = Field()
    full_name = Field()
    domain_company_inn_match = Field()
    yandex_rating = Field()
    working_hours = Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    reviews_count = Field()
    reviews = Field()
    place_in_search = Field()
    details = Field()
    details_num = scrapy.Field()
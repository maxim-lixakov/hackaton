# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class RusprofileItem(Item):
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
    place_in_search = Field()
    details = Field()
    details_num = Field()
    phone = Field()
    email = Field()
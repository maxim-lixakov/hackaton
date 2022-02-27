# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class RusprofileItem(Item):
    domain = Field()
    inn = Field()
    place_in_search = Field()
    authorized_capital = Field()
    grade = Field()
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
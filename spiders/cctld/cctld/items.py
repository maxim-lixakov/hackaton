from scrapy import Item, Field


class DomainItem(Item):
    domain = Field()
    inn = Field()
    place_in_search = Field()

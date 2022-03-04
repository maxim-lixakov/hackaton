from scrapy import Item, Field


class DomainItem(Item):
    domain = Field()
    inn = Field()
    place_in_search_yandex = Field()
    place_in_search_google = Field()
    title = Field()
    probable_name = Field()
    place_in_search = Field()
    details = Field()


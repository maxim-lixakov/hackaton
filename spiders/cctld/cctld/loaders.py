from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst


class DomainLoader(ItemLoader):
    default_output_processor = TakeFirst()

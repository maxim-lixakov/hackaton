from urllib.parse import urljoin
import json

from scrapy import Spider
from scrapy.http import Request

from cctld.items import DomainItem
from cctld.loaders import DomainLoader


class WhoisSpider(Spider):
    name = 'whois'
    base_url = 'https://cctld.ru/tci-ripn-rdap/domain/сантехник-а.рф'

    def start_requests(self):
        with open('search.jl') as f:
            for line in f.readlines():
                line = json.loads(line)
                yield Request(
                    url=urljoin(self.base_url, line['domain']),
                    callback=self.parse,
                    cb_kwargs=line,
                )

    def parse(self, response, **kwargs):
        entities = response.json().get('entities')
        loader = DomainLoader(DomainItem())
        for field in kwargs:
            loader.add_value(field, kwargs[field])
        if entities:
            inn = entities[1].get('ripn_tax_payer_number')
            if inn:
                loader.add_value('inn', inn)
                yield loader.load_item()

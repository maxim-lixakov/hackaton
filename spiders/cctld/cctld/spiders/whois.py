from urllib.parse import urljoin
import json

from scrapy import Spider
from scrapy.http import Request

from cctld.items import DomainItem
from cctld.loaders import DomainLoader


class WhoisSpider(Spider):
    name = 'whois'
    base_url = 'https://cctld.ru/tci-ripn-rdap/domain/'

    def start_requests(self):
        with open('result_of_yandex_search.jl') as f:
            for line in f.readlines():
                line = json.loads(line)
                yield Request(
                    url=urljoin(self.base_url, line['domain']),
                    callback=self.parse,
                )

    def parse(self, response, **kwargs):
        domain = response.json()['handle'].lower()
        entities = response.json().get('entities')
        if entities:
            inn = entities[1].get('ripn_tax_payer_number')
            if inn:
                loader = DomainLoader(DomainItem())
                loader.add_value('domain', domain)
                loader.add_value('inn', inn)
                yield loader.load_item()

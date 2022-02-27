import json
from urllib.parse import urljoin

import scrapy
from scrapy import Request

from rusprofile.items import RusprofileItem


class JuridicalInfoSpider(scrapy.Spider):
    name = 'juridical_info'
    allowed_domains = ['rusprofile']
    base_url = 'https://www.rusprofile.ru/search?query={}&type=ul'

    def start_requests(self):
        with open('result_of_whois.jl') as f:
            for line in f.readlines():
                line = json.loads(line)
                inn = line['inn']
                yield Request(
                    url=self.base_url.format(inn),
                    callback=self.parse,
                    cb_kwargs=line,
                )

    def parse(self, response, **kwargs):
        item = RusprofileItem()
        for field in kwargs:
            item[field] = kwargs[field]
        item['grade'] = response.xpath('//a[@class="rely-tile-badge rely-rating-positive"]/text()').get()
        item['date_reg'] = response.xpath('//dd[@itemprop="foundingDate"]/text()').get()
        item['authorized_capital'] = response.xpath('//dd[@class="company-info__text"]'
                                                    '/span[@class="copy_target"]/text()').get()
        item['ogrn'] = response.xpath('//span[@id="clip_ogrn"]/text()').get()
        item['activity'] = response.xpath('//div[@class="rightcol"]/'
                                          'div[@class="company-row"]/span[@class="company-info__text"]/'
                                          'text()').get()
        item['name'] = response.xpath('//h1[@itemprop="name"]/text()').get()
        item['director'] = response.xpath('//div[@class="company-row hidden-parent"]/'
                                          'span[@class="company-info__text"]/text()').get()
        item['fines'] = response.xpath('//div[@class="connexion-col__title tosmall"]/text()').get()
        item['planned_checks'] = response.xpath('//a[@class="num gtm_i_1"]/text()').get()
        item['unplanned_checks'] = response.xpath('//a[@class="num gtm_i_2"]/text()').get()
        if response.xpath('//a[@class="num gtm_i_3"]/text()'):
            item['infringement'] = response.xpath('//a[@class="num gtm_i_3"]/text()').getall()[0]
            item['not_infringement'] = response.xpath('//a[@class="num gtm_i_3"]/text()').getall()[1]
            item['unknown_infringement'] = response.xpath('//a[@class="num gtm_i_3"]/text()').getall()[1]
        yield item

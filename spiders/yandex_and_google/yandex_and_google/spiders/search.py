import re
import os
import zipfile

import scrapy

from yandex_and_google.items import DomainItem


class SearchSpider(scrapy.Spider):
    name = 'search'
    resources = set()
    place_in_search_yandex = 1
    place_in_search_google = 1

    def start_requests(self):
        dirname = os.getcwd()
        filename = os.path.join(dirname, 'data/poiskpostav_v1.xlsx')
        with zipfile.ZipFile(filename) as z:
            for filename in z.namelist():
                if 'sharedStrings' in filename:
                    with z.open(filename) as f:
                        # test because of ban
                        # for element in re.findall('<t>\*(.+?)</t>', f.read().decode()):
                        for element in re.findall('<t>\*(.+?)</t>', f.read().decode())[:1]:
                            text = re.sub('ГОСТ\s+\d+', '', element)
                            yield scrapy.Request(f'https://yandex.ru/search/?text={text}',
                                                 callback=self.parse, cb_kwargs={'search': 'yandex'})
                            google_url = f'https://www.google.com/search?q={text}' \
                                  '&aqs=chrome..69i57j0i546l2.223j0j7&sourceid=chrome&ie=UTF-8'
                            yield scrapy.Request(url=google_url, callback=self.parse, cb_kwargs={'search': 'google'})

    def parse(self, response, **kwargs):
        for resource in response.xpath('//a/@href').getall():
            link = re.findall('http[s]*:\/\/(?:www\.|)(.+?)\/', resource)
            if link:
                if link[0] not in self.resources:
                    item = DomainItem()
                    item['domain'] = link[0]
                    if kwargs['search'] == 'yandex':
                        item['place_in_search_yandex'] = self.place_in_search_yandex
                        self.place_in_search_yandex += 1
                    elif kwargs['search'] == 'google':
                        item['place_in_search_google'] = self.place_in_search_google
                        self.place_in_search_google += 1
                    self.resources.add(link[0])
                    url = f'https://{link[0]}'
                    yield scrapy.Request(url=url, callback=self.get_name, cb_kwargs={'item': item})

    def get_name(self, response, **kwargs):
        item = kwargs['item']
        item['title'] = response.xpath('//title/text()').get()
        probable_name = re.findall('(["]*ООО["]*\s[A-zА-Яа-я()]+)', response.text)
        if probable_name:
            item['probable_name'] = probable_name[0]
        yield item

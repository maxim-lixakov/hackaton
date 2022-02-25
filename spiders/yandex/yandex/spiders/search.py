import re
import os
import zipfile

import scrapy


class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['yandex.ru']
    start_urls = ['http://yandex.ru/']

    def start_requests(self):
        dirname = os.getcwd()
        filename = os.path.join(dirname, 'data\poiskpostav_v1.xlsx')
        with zipfile.ZipFile(filename) as z:
            for filename in z.namelist():
                if 'sharedStrings' in filename:
                    with z.open(filename) as f:
                        for element in re.findall('<t>\*(.+?)</t>', f.read().decode())[:2]:
                            text = re.sub('ГОСТ\s+\d+', '', element)
                            yield scrapy.Request(f'https://yandex.ru/search/?text={text}', callback=self.parse)

    def parse(self, response, **kwargs):
        content = response.body

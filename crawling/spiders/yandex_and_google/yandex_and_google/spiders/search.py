import json
import re
import os
import zipfile

import scrapy
from scrapy import signals

from yandex_and_google.items import DomainItem


class SearchSpider(scrapy.Spider):
    name = 'search'
    resources = {'yandex.ru', 'www.google.com', 'music.yandex.ru', 'maps.google.com'}
    skip = {'yandex.ru', 'www.google.com', 'music.yandex.ru', 'maps.google.com', 'market.yandex.ru',
            'passport.yandex.ru', 'pokupki.market.yandex.ru', 'yabs.yandex.ru', 'apps.apple.com',
            'Zaochnik.com', 'habr.com', 'emulek.github.io', 'Zaochnik.com' 'OZON.ru', 'appgallery.huawei.com'}
    data = dict()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(SearchSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        with open('search.jl', 'a') as f:
            for key in self.data:
                if len(self.data[key]) == 5:
                    item = {
                        "domain": key,
                        "place_in_search": int(min(self.data[key][1])),
                        "details_num": self.data[key][0],
                        "details": self.data[key][2],
                        "title": self.data[key][3],
                        "probable_name": self.data[key][4].get('name'),
                        "email": self.data[key][4].get('email'),
                        "phone": self.data[key][4].get('phone'),
                    }
                elif len(self.data[key]) == 4:
                    item = {
                        "domain": key,
                        "place_in_search": int(min(self.data[key][1])),
                        "details_num": self.data[key][0],
                        "details": self.data[key][2],
                        "title": self.data[key][3],
                    }
                else:
                    item = {
                        "domain": key,
                        "place_in_search": int(min(self.data[key][1])),
                        "details": self.data[key][2],
                        "details_num": self.data[key][0],
                    }
                f.write(json.dumps(item) + '\n')

    def start_requests(self):
        dirname = os.getcwd()
        filename = os.path.join(dirname, 'data/poiskpostav_v1.xlsx')
        with zipfile.ZipFile(filename) as z:
            for filename in z.namelist():
                if 'sharedStrings' in filename:
                    with z.open(filename) as f:
                        # test because of ban
                        # for element in re.findall('<t>\*(.+?)</t>', f.read().decode()):
                        for element in re.findall('<t>\*(.+?)</t>', f.read().decode()):
                            text = re.sub('ГОСТ\s+\d+', '', element)
                            yield scrapy.Request(f'https://yandex.ru/search/?text={text}',
                                                 callback=self.parse, cb_kwargs={'search': 'yandex',
                                                                                 'detail': element})
                            google_url = f'https://www.google.com/search?q={text}' \
                                  '&aqs=chrome..69i57j0i546l2.223j0j7&sourceid=chrome&ie=UTF-8'
                            yield scrapy.Request(url=google_url, callback=self.parse, cb_kwargs={'search': 'google',
                                                                                                 'detail': element})
                            commercial_search = 'https://yandex.ru/search/direct?text={}&filters_docs=direct_cm&lr=213'
                            yield scrapy.Request(url=commercial_search,
                                                 callback=self.parse, cb_kwargs={'search': 'com',
                                                                                 'detail': element})

    def parse(self, response, **kwargs):
        place_in_search_yandex = 1
        place_in_search_google = 1
        for resource in response.xpath('//a/@href').getall():
            link = re.findall('http[s]*:\/\/(?:www\.|)(.+?)\/', resource)
            if link:
                if 'googl' in link[0] or 'yand' in link[0]:
                    continue
                if link[0] not in self.resources and link[0] not in self.skip:
                    item = DomainItem()
                    item['domain'] = link[0]
                    if kwargs['search'] == 'yandex':
                        self.data[link[0]] = [1, [place_in_search_yandex], [kwargs['detail']]]
                        item['place_in_search_yandex'] = place_in_search_yandex
                        item['commercial_search'] = 0
                        place_in_search_yandex += 1
                    elif kwargs['search'] == 'google':
                        self.data[link[0]] = [1, [place_in_search_google], [kwargs['detail']]]
                        item['place_in_search_google'] = place_in_search_google
                        item['commercial_search'] = 0
                        place_in_search_google += 1
                    else:
                        self.data[link[0]] = [1, [place_in_search_yandex], [kwargs['detail']]]
                        item['commercial_search'] = 1
                    self.resources.add(link[0])
                    url = f'https://{link[0]}'
                    yield scrapy.Request(url=url, callback=self.get_name, cb_kwargs={'item': item})
                elif link[0] in self.resources and link[0] not in self.skip:
                    if kwargs['detail'] not in self.data[link[0]][2]:
                        if kwargs['search'] == 'yandex':
                            self.data[link[0]][0] += 1
                            self.data[link[0]][1].append(place_in_search_yandex)
                            self.data[link[0]][2].append(kwargs['detail'])
                            place_in_search_yandex += 1
                        if kwargs['search'] == 'google':
                            self.data[link[0]][0] += 1
                            self.data[link[0]][1].append(place_in_search_google)
                            self.data[link[0]][2].append(kwargs['detail'])
                            place_in_search_google += 1
                    else:
                        if kwargs['search'] == 'yandex':
                            self.data[link[0]][1].append(place_in_search_yandex)
                            place_in_search_yandex += 1
                        if kwargs['search'] == 'google':
                            self.data[link[0]][1].append(place_in_search_google)
                            place_in_search_google += 1

    def get_name(self, response, **kwargs):
        item = kwargs['item']
        item['title'] = response.xpath('//title/text()').get()
        probable_name = re.findall('(["]*ООО["]*\s[A-zА-Яа-я()]+)', response.text)
        self.data[item['domain']].append(response.xpath('//title/text()').get())
        if probable_name:
            item['probable_name'] = probable_name[0]
        for endpoint in ['contacts/',
                         'kontacts/',
                         'page/contacts/',
                         'company/coordinates',
                         'contact/',
                         'contakty/',
                         'contacts/',
                         'contacts.html/',
                         'kontakty/',
                         'kontakti/',
                         'address/',
                         'contacts/head-office/',
                         'content/6-kontakty/',
                         'index.php?route=content/contact/',
                         'index.php/ru/kontakty/',
                         'content/6-kontakt-info/',
                         'content/kontakt-info/',
                         'about/contacts/',
                         'contact-us/',
                         'contacts/russia/',
                         'info/contacts/',
                         'Contacts.aspx/',
                         'kontakty/ofis/',
                         'контакт/',
                         'proezd/',
                         'about/kontakty/',
                         'content/contacts/',
                         'adres/',
                         'карта_и_контакты/',
                         'index/kontakty/0-4/',
                         'company/contacts/',
                         'pages/contact-us/',
                         'kontakty.html/',
                         'nashi_kontaki/',
                         'контакты/',
                         ]:
            if len(self.data[item['domain']]) > 4:
                break
            url = f'https://{item["domain"]}/{endpoint}'
            yield scrapy.Request(url=url, callback=self.parse_contacts, cb_kwargs={'item': item})

    def parse_contacts(self, response, **kwargs):
        item = kwargs['item']
        emails = re.findall('(\w*@\w*\.\w*)', response.text)
        phones = re.findall('([8|\+7)-?]?\[?\d{3}\]?-?\d{1}-?\d{1}-?\d{1}-?\d{1}-?\d{1}-?\d{1}-?\d{1})',
                            response.text)
        name = None
        if len(re.findall('(["]*ООО["]*\s[A-zА-Яа-я()]+)', response.text)) > 0:
            name = re.findall('(["]*ООО["]*\s[A-zА-Яа-я()]+)', response.text)[0]
        email = None
        if len(emails) > 0:
            email = emails[len(emails) // 2]
        phone = None
        if len(phones) > 0:
            phone = phones[len(phones) // 2]
        data = {'email': email, 'phone': phone, 'name': name}
        self.data[item['domain']].append(data)
        yield item
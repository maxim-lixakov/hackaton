import json

from scrapy import Request, Spider

from yandex_and_google.items import CompanyInfoItem


class CompanyInfoSpider(Spider):
    name = 'company_info'
    allowed_domains = ['yandex.ru']
    base_url = 'https://yandex.ru/search/?text={}&clid=2270455&banerid=0702004852%3ASW-7fec14d3653b&win=527&lr=213'

    def start_requests(self):
        with open('result_of_rusprofile.jl') as f:
            for line in f.readlines():
                line = json.loads(line)
                name = line['full_name']
                yield Request(
                    url=self.base_url.format(name),
                    callback=self.parse,
                    cb_kwargs=line,
                )

    def parse(self, response, **kwargs):
        rating_page = response.xpath('//div[contains(@class, "content__right content")]').get()
        item = CompanyInfoItem()
        if rating_page:
            yandex_rating = response.xpath('//div[contains(@class, "RatingVendor")]/text()').get()
            working_hours = response.xpath('//span[contains(@class, "OrgContacts-ItemContent")]/text()').get()
            phone = response.xpath('//span[contains(@class, "OrgContacts-Phone")]/@aria-label').get()
            reviews = response.xpath('//div[@class="Reviews-TitleWrapper"]').get()
            if reviews:
                reviews_count = response.xpath('//div[@class="Reviews-TitleWrapper"]/'
                                               'div[contains(@class,"Reviews-Title")]/span/@aria-label').get()
                reviews = response.xpath('//div[@aria-label="Отзывы"]//div[contains(@class,"TextCut")]'
                                         '//span[@class="Cut-Visible"]/text()').getall()
                item['reviews_count'] = reviews_count
                item['reviews'] = reviews
            item['yandex_rating'] = yandex_rating
            item['working_hours'] = working_hours
            item['phone'] = phone
        for field in kwargs:
            item[field] = kwargs[field]
        yield item

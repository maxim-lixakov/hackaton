import json

from scrapy import Request, Spider
# import pdfplumber
import re

from egrul.items import EgrulItem


def try_to_find(pattern, text):
  try:
    value = re.findall(pattern, text)[0]
  except IndexError:
    value = ''
  return value


def lcs(X, Y):
    # найти длину строк
    m = len(X)
    n = len(Y)
    L = [[None] * (n + 1) for i in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    # L [m] [n] содержит длину LCS из X [0..n-1] & Y [0..m-1]

    return L[m][n]


class EgrulInfoSpider(Spider):
    name = 'egrul_info'
    allowed_domains = ['egrul.nalog.ru']

    def start_requests(self):
        with open('result_of_whois.jl') as f:
            # test because of ban
            # for line in f.readlines():
            for line in f.readlines()[:5]:
                line = json.loads(line)
                domain_inn = line['inn']
                data = {'query': domain_inn}
                yield Request('https://egrul.nalog.ru/', method='POST', callback=self.parse_0_id, cb_kwargs=line,
                               body=json.dumps(data), headers={'Content-Type': 'application/json'})

    def parse_0_id(self, response, **kwargs):
        item = EgrulItem()
        for field in kwargs:
            item[field] = kwargs[field]
        pdf_id = response.json().get('t')
        if not pdf_id:
            yield item
        else:
            url = f'https://egrul.nalog.ru/search-result/{pdf_id}'
            yield Request(url=url, callback=self.parse_1_id,
                          cb_kwargs={'item': item, 'pdf_id': pdf_id})

    def parse_1_id(self, response, **kwargs):
        try:
            pdf_id = response.json()['rows'][0]['t']
            url = f'https://egrul.nalog.ru/vyp-download/{pdf_id}'
            item = kwargs['item']
            item['full_name'] = response.json().get('rows')[0]['n']
            item['ogrn'] = response.json().get('rows')[0]['o']
            item['director'] = response.json().get('rows')[0]['g']
            item['inn'] = response.json().get('rows')[0]['i']
        except IndexError:
            pdf_id = response.json()['rows']['t']
            url = f'https://egrul.nalog.ru/vyp-download/{pdf_id}'
            item = kwargs['item']
            item['full_name'] = response.json().get('rows')['n']
            item['ogrn'] = response.json().get('rows')['o']
            item['director'] = response.json().get('rows')['g']
            item['inn'] = response.json().get('rows')['i']
        except KeyError:
            pass
        if 'probable_name' in item:
            if lcs(item['probable_name'], item['full_name']) > 4:
                item['domain_company_inn_match'] = 1
            else:
                item['domain_company_inn_match'] = 0
                data = {'query': item['probable_name']}
                yield Request('https://egrul.nalog.ru/', method='POST', callback=self.parse_0_id,
                              cb_kwargs={'item': item},
                              body=json.dumps(data), headers={'Content-Type': 'application/json'},
                              dont_filter=True)
        else:
            if 'title' in item:
                if lcs(item['title'], item['full_name']):
                    item['domain_company_inn_match'] = 1
                else:
                    item['domain_company_inn_match'] = 0
        yield item
        # yield Request(url=url, callback=self.parse,
        #               cb_kwargs={'item': kwargs['item'], 'pdf_id': pdf_id})

    def parse(self, response, **kwargs):
        # response = response.json()
        with open(f'/content/{kwargs["pdf_id"]}/data.pdf', 'wb') as f:
            f.write(response.content)
        file_path = f'/content/{kwargs["pdf_id"]}/data.pdf'
        with pdfplumber.open(file_path) as pdf:
            text = []
            for page in pdf.pages:
                # text.append(page.extract_text())
                text.append(' '.join(page.extract_text().split('\n')))
        text = ' '.join(text)
        company = {}
        company['name'] = try_to_find('Сокращенное наименование на русском (\w{3} ".*?")', text)
        company['inn'] = try_to_find('ИНН юридического лица (\d+)', text)
        company['ogrn'] = try_to_find('ОГРН (\d{13})', text)  # PSRN
        company['registration_date'] = try_to_find('Дата регистрации (\d{2}.\d{2}.\d{4})', text)
        if not company['registration_date']:
            company['registration_date'] = try_to_find('Дата присвоения ОГРН (\d{2}.\d{2}.\d{4})', text)
        company['authorized_capital'] = try_to_find('Размер \(в рублях\) (\d+)', text)
        company['basic_activity'] = try_to_find(
            'Сведения об основном виде деятельности .{36} Код и наименование вида деятельности \d{2}.\d{2}(.{2}\D*)',
            text).strip(r' .1-9')
        print(company)

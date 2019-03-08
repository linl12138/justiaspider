# -*- coding: utf-8 -*-
import scrapy
import re
from court.items import CourtItem

class CourtSccaSpider(scrapy.Spider):
    name = 'court_scca'
    allowed_domains = ['court.com']
    start_urls = []
    for i in range(2001, 2020):
        # if i < 2001:
            # for j in range(300):
            #     start_urls.append('https://www.courts.gov.bc.ca/jdb-txt/sc/' + '%02d' % (i % 100) + '/00/s' + '%02d' % (i % 100) + '-%04d' % j + '.htm')
            #     start_urls.append('https://www.courts.gov.bc.ca/jdb-txt/ca/' + '%02d' % (i % 100) + '/00/c' + '%02d' % (1 % 100) + '-%04d' % j + '.htm')
        # else:
        for j in range(3000):
            start_urls.append('https://www.courts.gov.bc.ca/jdb-txt/sc/' + '%02d' % (i % 100) + '/' + '%02d' % (j / 100) + '/' + str(i) + 'BCSC' + '%04d' % j + '.htm')
            start_urls.append('https://www.courts.gov.bc.ca/jdb-txt/ca/' + '%02d' % (i % 100) + '/' + '%02d' % (j / 100) + '/' + str(i) + 'BCCA' + '%04d' % j + '.htm')
    def parse(self, response):
        item = CourtItem()
        item['url'] = response.url
        item['title'] = response.xpath('//title/text()').extract_first()
        if re.match(r'(.*Not Found.*)', item['title']):
            return
        item['txt'] = ''
        for txt in response.xpath('//p//text()').extract():
            item['txt'] += txt
        yield item
        pass

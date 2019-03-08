# -*- coding: utf-8 -*-
import scrapy
from austlii.items import AustliiItem
from scrapy import Request
import re


class AustliisSpider(scrapy.Spider):
    name = 'austliis'
    start_urls = []
    court_list = ['cth', 'act', 'nsw', 'nt', 'qld', 'sa', 'tas', 'vic', 'wa']
    co_list = ['CA', 'SC', 'SCFC']
    for i in court_list:
        if i == 'cth':
            for ch in range(65, 91):
                url = 'http://www8.austlii.edu.au/cgi-bin/viewtoc/au/cases/' + i + '/HCA' + '/toc-' + chr(ch) + '.html'
                start_urls.append(url)
        else:
            for j in co_list:
                for ch in range(65, 91):
                    url = 'http://www8.austlii.edu.au/cgi-bin/viewtoc/au/cases/' + i + '/' + i.upper() + j + '/toc-' + chr(ch) + '.html'
                    start_urls.append(url)

    def parse(self, response):
        url = response.url
        if re.findall('[0-9]+\.html', url):
            item = AustliiItem()
            item['link'] = url
            title = response.xpath('//h1/text()').extract()
            item['title'] = title[0]
            yield item
        else:
            base_url = 'http://www8.austlii.edu.au'
            search_url = response.xpath('//a/@href').re('.*[0-9]{4}/[0-9]+.html')
            for i in search_url:
                yield Request(base_url + i, callback=self.parse)
        pass

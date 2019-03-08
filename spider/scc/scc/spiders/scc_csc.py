# -*- coding: utf-8 -*-
import scrapy
from scc.items import SccItem


class SccCscSpider(scrapy.Spider):
    name = 'scc_csc'
    start_urls = []
    for i in range(0, 18000):
        url = 'https://scc-csc.lexum.com/scc-csc/scc-csc/en/item/' + str(i) + '/index.do'
        start_urls.append(url)

    def parse(self, response):
        title = response.xpath('//p//text()').re(r'.* v\. .*')
        if title:
            item = SccItem()
            item['title'] = title[0]
            item['link'] = response.url
            item['country'] = 'Canada'
            print response.url
            yield item
        pass

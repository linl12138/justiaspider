# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from kr.items import KrsItem
import re

class KrsSpider(scrapy.Spider):
    name = 'krs'
    start_urls = []
    for i in range(1, 22):
        start_urls.append('http://www.scourt.go.kr/region/location/RegionLocationListAction.work?pageIndex=' + str(i))

    def parse(self, response):
        route = '/dcboard/new/DcNewsListAction.work?gubun=44&pageIndex=1'
        sub_courts = response.xpath('//*[@id="content"]/div[2]/table/tbody/tr/td[4]/a/@href').re('(.*\.scourt\.go\.kr)')
        for url in sub_courts:
            if url != 'http://www.scourt.go.kr':
                print url
                yield Request(url + route, callback = self.data_parse)
        pass

    def data_parse(self, response):
        url = re.findall(r'(.*)/dcboard/.*', response.url)
        url = url[0]
        titles = response.xpath('//*[@id="print_preview_html"]/div/div[1]/table/tbody/tr/td[2]/a/text()').extract()
        links = response.xpath('//*[@id="print_preview_html"]/div/div[1]/table/tbody/tr/td[2]/a/@href').extract()
        if titles:
            item = KrsItem()
            for i in range(len(titles)):
                item['title'] = titles[i].replace('\r', '').replace('\n', '').replace('\t', '')
                item['country'] = 'Korea'
                item['link'] = url + links[i]
                yield item
            pages = re.findall(r'.*pageIndex=(.*)', response.url)
            page = int(pages[0])
            yield Request(url + '/dcboard/new/DcNewsListAction.work?gubun=44&pageIndex=' + str(page + 1), callback = self.data_parse)
        pass

# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from arbitr.items import ArbitrItem
import re


class ArbitrsSpider(scrapy.Spider):
    name = 'arbitrs'
    start_urls = ['https://vsrf.ru/lk/practice/cases?&numberExact=true&registerDateExact=off&caseType=ECONOMIC&considerationDateExact=off&ajax=true&page=1']

    def parse(self, response):
        if 'page' in response.url:
            data_url = response.xpath('//a/@href').re(r'.*number.*')
            for url in data_url:
                next_url = url.replace('http://', 'http://m.')
                yield Request(next_url, callback = self.parse, dont_filter = True)
            if data_url:
                page = re.findall(r'.*page=([0-9]+)', response.url, re.I)
                page = int(page[0])
                print '!!!page' + str(page) + '!!!'
                next_url = re.findall(r'(.*page=)[0-9]+', response.url, re.I)
                yield Request(next_url[0] + str(page + 1), callback = self.parse, dont_filter = True)
        elif 'Card?number' in response.url:
            item = ArbitrItem()
            plaintiffs = []
            defendants = []
            flag = 1
            plaintiff = response.xpath('//*[@id="container"]/div[3]/ul[2]/li[' + str(flag) + ']//text()').extract()
            plaintiffs += plaintiff
            while plaintiff:
                flag += 1
                plaintiff = response.xpath('//*[@id="container"]/div[3]/ul[2]/li[' + str(flag) + ']//text()').extract()
                plaintiffs += plaintiff
            item['plaintiff'] = ','.join(plaintiffs)
            flag = 1
            defendant = response.xpath('//*[@id="container"]/div[3]/ul[3]/li[' + str(flag) + ']//text()').extract()
            defendants += defendant
            while defendant:
                flag += 1
                defendant = response.xpath('//*[@id="container"]/div[3]/ul[3]/li[' + str(flag) + ']//text()').extract()
                defendants += defendant
            item['defendant'] = ','.join(defendants)
            if item['plaintiff'] and item['defendant']:
                item['title'] = item['plaintiff'] + ' v. ' + item['defendant']
            else:
                return
            item['link'] = response.url
            item['country'] = 'Russia'
            yield item
        pass

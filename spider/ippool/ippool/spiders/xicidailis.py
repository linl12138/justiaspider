# -*- coding: utf-8 -*-
import scrapy
from ippool.items import IppoolItem


class XicidailisSpider(scrapy.Spider):
    name = 'xicidailis'
    start_urls = []
    for i in range(1, 3601):
        start_urls.append('https://www.xicidaili.com/nn/' + str(i))

    def parse(self, response):
        index = 2
        ip = response.xpath('//*[@id="ip_list"]/tr[' + str(index) + ']/td[2]/text()').extract()
        port = response.xpath('//*[@id="ip_list"]/tr[' + str(index) + ']/td[3]/text()').extract()
        speed = response.xpath('//*[@id="ip_list"]/tr[' + str(index) + ']/td[7]/div/@title').re(r'[0-9\.]*')
        live = response.xpath('//*[@id="ip_list"]/tr[' + str(index) + ']/td[9]/text()').extract()
        while ip:
            if float(speed[0]) < 0.2 and live and not '\u5206\u949f' in live[0]:
               item = IppoolItem()
               item['ip'] = ip[0] + ':' + port[0]
               yield item
            index += 1
            ip = response.xpath('//*[@id="ip_list"]/tr[' + str(index) + ']/td[2]/text()').extract()
            port = response.xpath('//*[@id="ip_list"]/tr[' + str(index) + ']/td[3]/text()').extract()
            speed = response.xpath('//*[@id="ip_list"]/tr[' + str(index) + ']/td[7]/div/@title').re(r'[0-9\.]*')
            live = response.xpath('//*[@id="ip_list"]/tr[' + str(index) + ']/td[9]/div/@title').re(r'[0-9\.]*')
        pass

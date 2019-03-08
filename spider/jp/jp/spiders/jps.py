# -*- coding: utf-8 -*-
import scrapy
from jp.items import JpsItem
from scrapy import Request


class JpsSpider(scrapy.Spider):
    name = 'jps'
    start_urls = ['http://www.courts.go.jp/app/hanrei_jp/list1?page=1745&sort=1&filter%5BjudgeDateMode%5D=2&filter%5BjudgeGengoFrom%5D=%E6%98%AD%E5%92%8C&filter%5BjudgeYearFrom%5D=1&filter%5BjudgeMonthFrom%5D=1&filter%5BjudgeDayFrom%5D=1&filter%5BjudgeGengoTo%5D=%E5%B9%B3%E6%88%90&filter%5BjudgeYearTo%5D=31&filter%5BjudgeMonthTo%5D=2&filter%5BjudgeDayTo%5D=21']

    def parse(self, response):
        item = JpsItem()
        url = 'http://www.courts.go.jp'
        titles = response.xpath('//*[@id="list"]/table/tr/td[2]/text()').extract()
        links = response.xpath('//*[@id="list"]/table/tr/td[3]/a/@href').extract()
        for i in range(len(links)):
            item['title'] = (titles[2 * i] + titles[i * 2 + 1]).replace('\n', '').replace('\t', '').strip()
            item['link'] = url + links[i]
            item['country'] = 'Japan'
            yield item
        if len(links) == 10:
            next_url = response.xpath('//*[@id="search_content"]/div[1]/div[1]/a/@href').re(r'.*page.*')
            yield Request(url + next_url[-1], callback = self.parse)
        pass

# -*- coding: utf-8 -*-
import scrapy
from highsingapore.items import HighsingaporeItem
from scrapy.selector import Selector


class HighcourtSpider(scrapy.Spider):
    name = 'highcourt'
    allowed_domains = ['singaporelawwatch.sg']
    start_urls = ['https://www.singaporelawwatch.sg/Judgments/High-Court']
    headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}

    def parse(self, response):
        addrs = list(response.xpath('//div[@class = "edn_401_article_list_wrapper"]/article[@class = "edn_clearFix edn_simpleList"]').extract())
        #addrs = response.css('.edn_clearFix edn_simpleList')
        #addrs = response.css('.edn_399_article_list_wrapper .edn_clearFix edn_simpleList')
        for addr in addrs:
            print(addr)
            addr = Selector(text = addr)
            item = HighsingaporeItem()
            item['country'] = "singapore"
            item['court'] = "high court"
            item['title'] = addr.xpath('//h3/a/text()').extract_first().replace('\t','').replace('\r','').replace('\n','').strip()
            item['link'] = addr.xpath('//h3/a/@href').extract_first()
            yield item

        next_page = response.xpath('//div[@class = "article_pager"]').css('a::attr(href)').extract()
        next_page = next_page[len(next_page)-2]
        yield scrapy.Request(url = next_page,headers = self.headers,callback = self.parse)


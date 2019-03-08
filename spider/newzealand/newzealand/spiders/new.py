# -*- coding: utf-8 -*-
import scrapy
from newzealand.items import NewzealandItem
from scrapy.selector import Selector


class NewSpider(scrapy.Spider):
    name = 'new'
    allowed_domains = ['courtsofnz.govt.nz']


    def start_requests(self):
        base_url = "http://www.courtsofnz.govt.nz/the-courts/supreme-court/case-summaries/case-information-"
        for i in range(2004,2020):
            url = base_url + str(i)
            yield scrapy.Request(url =url,callback = self.parse)

    def parse(self, response):
        item = NewzealandItem()
        tables = response.xpath('//table[@class = "case-block"]').extract()
        for table in tables:
            table = Selector(text = table)
            item['country'] = "New Zealand"
            item['case_num'] = table.xpath('//tr/td/p/text()').extract_first()
            item['case_name'] = table.xpath('//tbody/tr/td/p/text()').extract_first()
            item['summary'] = table.xpath('//tbody/tr/td/p/text()').extract()[1]
            yield item


# -*- coding: utf-8 -*-
import scrapy


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'seair'
    start_urls = [
        "https://www.seair.co.in/global-trade-data/argentina-import-data.aspx"
    ]

    def parse(self, response):
        yield {
            'url': response.url,
            'hd': response.xpath('//tr/th/text()|//tr/td/text()').extract()
        }
        next_page_urls = response.xpath("//a/@href").extract()
        for next_page_url in next_page_urls:
            if next_page_url is not None:
                yield scrapy.Request(response.urljoin(next_page_url))


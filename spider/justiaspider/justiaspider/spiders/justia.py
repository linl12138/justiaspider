# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from justiaspider.items import JustiaItem
from scrapy import Request
from time import sleep


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'justia'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Mobile Safari/537.36'
    }
    allowed_domains = ['dockets.justia.com/']
    #start_urls = ["https://dockets.justia.com/browse/state-nevada"]
#states_names = ['oregon']
    states_names = ['alabama', 'alaska', 'arizona', 'california', 'colorado', 'delaware',
                    'connecticut', 'district_of_columbia', 'florida', 'georgia', 'hawaii', 'idaho', 'illinois',
                    'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts',
                    'michigan', 'minnesota', 'missouri', 'montana', 'nebraska', 'nevada', 'new_hampshire',
                    'new_jersey', 'new_mexico', 'new_york', 'north_carolina', 'north_dakota', 'ohio', 'oklahoma',
                    'oregon', 'pennsylvania', 'rhode_island', 'south_carolina', 'south_dakota', 'tennessee',
                    'texas', 'utah', 'vermont', 'virginia', 'washington', 'west_virginia', 'wisconsin',
                    'wyoming', 'guam', 'mariana_islands', 'puerto_rico']
    '''start_urls = []
                        states_url = "https://dockets.justia.com/browse/state-"
                        for state in states_names:
                        full_urls = states_url + str(state)
                        start_urls.append(full_urls)
                        print(start_urls)'''

    def start_requests(self):
        states_url = "https://dockets.justia.com/browse/state-"
        for state in self.states_names:
            url = states_url + str(state)
            print(url)
            yield Request(url,headers = self.headers,callback = self.parse_states,dont_filter = True)

    def parse_states(self,response):
        base_url = "https://dockets.justia.com"
        addrs = response.xpath('//div[@class = "has-padding-content-block-30 -zb"]').xpath('//a[@class = "case-name"]/@href').extract()[0:20]
        next_page = list(response.xpath('//div[@class = "pagination to-large-font"]').css('a::attr(href)').extract())
        next_last = next_page[len(next_page)-1]
        u_url = base_url+next_last
        print(u_url)
        yield Request(url = u_url,callback = self.parse_states,dont_filter = True)
        for addr in addrs:
            print(addr)
            yield Request(url = addr,callback = self.parse,dont_filter = True)

    def parse(self,response):
        item = JustiaItem()
        if response:
            item['country'] = 'USA'
            item['title'] = response.xpath('//div[@class = "title-wrapper"]/h1[@class = "heading-1"]/text()').extract_first()
            item['plaintiff'] = response.xpath('//td[@class = "has-no-border"]/text()').extract_first()
            item['defendant'] = response.xpath('//td[@class = "has-no-border"]/text()').extract()[1]
            item['case_num'] = response.xpath('//td[@class = "has-no-border"]/text()').extract()[2]
            item['filed'] = response.xpath('//td[@class = "has-no-border"]/text()').extract()[3]
            item['court'] = response.xpath('//td[@class = "has-no-border"]/text()').extract()[4]
            item['Presiding_Judge'] = response.xpath('//td[@class = "has-no-border"]/text()').extract()[5]
            item["nature_suit"] = response.xpath('//td[@class = "has-no-border"]/text()').extract()[6]
            item["cause_action"] = response.xpath('//td[@class = "has-no-border"]/text()').extract()[7]
            item["jury_demanded"] = response.xpath('//td[@class = "has-no-border"]/text()').extract()[:-1]

            yield item
        else:
            print("return response fail")












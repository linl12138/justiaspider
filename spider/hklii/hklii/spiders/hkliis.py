# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from hklii.items import HkliiItem
import re


class HkliisSpider(scrapy.Spider):
    name = 'hkliis'
    start_urls = []
    for i in range(1995, 2020):
        tmp = 'http://www.hklii.hk/chi/hk/cases/hkcfi/' + str(i) + '/'
        start_urls.append(tmp)
    def parse(self, response):
        url = response.url
        if not 'html' in url:
            yearObj = re.findall(r'[0-9]{4}', url)
            year = yearObj[0]
            data_pages = response.xpath('//a/@href').extract()
            for data_page_url in data_pages:
                if year in data_page_url:
                    yield Request(url + data_page_url[8:], callback = self.parse)
        else:
            item = HkliiItem()
            case_num = response.xpath('//p/text()').re(r'([A-Z]* *[0-9]*/[0-9]{4})|([A-Z]* *[0-9]*/[0-9]{2})')
            plain_defen = response.xpath('//td[@valign="top"]//text()').re(u'\n?([\u4E00-\u9FA5a-zA-Z].*[\u4E00-\u9FA5a-zA-Z]|[\u4E00-\u9FA5a-zA-Z]).*?')
            item['title'] = response.xpath('//h2/text()').extract_first().replace('\n', '').strip()
            item['link'] = url
            item['case_num'] = case_num[0]
            if plain_defen[2] == u'\u8a34' or plain_defen[2] == u'\u5c0d' or plain_defen[2] == u'\u53ca' or plain_defen[2] == u'\u8207':
                if not u'\u7533\u8acb\u4eba' in plain_defen[1] and not u'\u7533\u8acb\u4eba' in plain_defen[4] and not u'\u7b54\u8faf\u4eba' in plain_defen[1] and not u'\u7b54\u8faf\u4eba' in plain_defen[4] and not u'\u539f\u544a\u4eba' in plain_defen[1]  and not u'\u88ab\u544a\u4eba' in plain_defen[4]:
                    item['plaintiff'] = plain_defen[1].strip('()[]')
                    item['defendant'] = plain_defen[4].strip('()[]')
            else:
                plain_defen = response.xpath('//td//text()').re(u'\n?([\u4E00-\u9FA5a-zA-Z].*[\u4E00-\u9FA5a-zA-Z]|[\u4E00-\u9FA5a-zA-Z]).*?')
                for idx, val in enumerate(plain_defen):
                    if val == u'\u8a34' or val == u'\u5c0d' or val == u'\u53ca' or val == u'\u8207':
                        if not u'\u7533\u8acb\u4eba' in plain_defen[idx - 1] and not u'\u7533\u8acb\u4eba' in plain_defen[idx + 2] and not u'\u7b54\u8faf\u4eba' in plain_defen[idx - 1] and not u'\u7b54\u8faf\u4eba' in plain_defen[idx + 2] and not u'\u539f\u544a\u4eba' in plain_defen[idx - 1]  and not u'\u88ab\u544a\u4eba' in plain_defen[idx + 2]:
                            item['plaintiff'] = plain_defen[idx - 1].strip('()[]')
                            item['defendant'] = plain_defen[idx + 2].strip('()[]')
                        break
            yield item
        pass

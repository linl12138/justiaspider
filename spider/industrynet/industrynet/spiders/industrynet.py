from scrapy.spiders import Spider
from scrapy import Request
from industrynet.items import IndustrynetItem

class IndustrynetSpider(Spider):
    name = 'industrynetSpider'
    download_delay = 5.0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://www.industrynet.com/companies'
        yield Request(url, headers=self.headers)

    def string_parser(self, value):
        if value:
            return value[0].strip()
        return ''

    def parse(self, response):
        item = IndustrynetItem()
        name = self.string_parser(response.xpath('//h1[@class="header2font bluetext"]/text()').extract())

        if name != '':
            addrs = response.xpath('//div[@style="float:left; overflow: hidden; width:320px; margin-left: 10px; margin-right: 10px;"]/text()').re(r'.*(?<!\s)$')
            base_url = 'https://www.industrynet.com'
            item['physical_address'] = ''
            for i in range(4):
                if i < len(addrs):
                    item['physical_address'] += addrs[i].strip()

            item['mailing_address'] = ''
            for i in range(4, 7):
                if i < len(addrs):
                    item['mailing_address'] += addrs[i].strip()


            item['phone'] = self.string_parser(response.xpath('//span[@id="listing_phoneshown"]/text()').extract())
            item['name'] = name
            item['capabilities'] = self.string_parser(response.xpath('//a[@href="/suppliers/FO0155/food-importers"]/text()').extract())
            item['brands'] = self.string_parser(response.xpath('//h4[@style="float:left; overflow: hidden; width:540px; margin-left: 10px; margin-right: 10px;"]/text()').extract())
            item['sic'] = self.string_parser(response.xpath('//h4[@style="float:left; overflow: hidden; width:500px; margin-left: 10px; margin-right: 10px;"]/text()').extract())

            yield item

        next_pages = response.xpath('//div[@style="float:left; overflow: hidden; width:500px; margin-left: 10px; margin-right: 10px;"]/a/@href').re(r'^(?!/companies).*$')
        for next_page_url in next_pages:
            if next_page_url is not None:
                yield Request(base_url + next_page_url, headers = self.headers, callback=self.parse)

        next_pages = response.xpath('//span[@class="browseletter"]/a/@href').extract()
        for next_page_url in next_pages:
            if next_page_url is not None:
                yield Request(base_url + next_page_url, headers = self.headers, callback=self.parse)

        next_pages = response.xpath('//span[@class="bodyfont"]/a/@href').extract()
        for next_page_url in next_pages:
            if next_page_url is not None:
                yield Request(base_url + next_page_url, headers = self.headers, callback=self.parse)

        next_pages = response.xpath('//div[@class="bodyfont"]/a/@href').extract()
        for next_page_url in next_pages:
            if next_page_url is not None:
                yield Request(base_url + next_page_url, headers = self.headers, callback=self.parse)

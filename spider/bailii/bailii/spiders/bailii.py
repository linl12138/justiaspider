from scrapy.spiders import Spider
from scrapy import Request
from bailii.items import BailiiItem

class BailiiSpider(Spider):
    name = 'bailiiSpider'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'https://www.bailii.org/indices/all-cases-0001.html'
        yield Request(url, headers=self.headers)

    def string_parser(self, value):
        if value:
            return value[0].strip()
        return ''

    def parse(self, response):
        item = BailiiItem()
        title = self.string_parser(response.xpath('//title/text()').extract())

        if title != []:
            item['title'] = title
            links = response.xpath('//a/@href').extract()
            for l in links:
                l = l.strip()
                if l.endswith('pdf'):
                    item['link'] = "https://www.bailii.org" + l
                    break

            yield item

        next_pages = response.xpath('//li/a/@href').extract()
        for next_page_url in next_pages:
            if next_page_url is not None:
                yield Request('https://www.bailii.org' + next_page_url, headers = self.headers, callback=self.parse)

        next_page = self.string_parser(response.xpath('//a[contains(.,"Next")]/@href').extract())
        if next_page != '':
            yield Request('https://www.bailii.org/indices/' + next_page, headers = self.headers, callback=self.parse)

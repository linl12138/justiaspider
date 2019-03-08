import scrapy


class MofanSpider(scrapy.Spider):
    name = "mofan"
    start_urls = [
        'https://www.seair.co.in/led-light-export-data.aspx',
    ]

    def parse(self, response):
        yield {     # return some results
            'description': response.xpath('//td[@itemprop="Item-Description"]').extract()
        }
        urls = response.css('a::attr(href)').re(r'^/.+?/$')     # find all sub urls
        for url in urls:
            yield response.follow(url, callback=self.parse)

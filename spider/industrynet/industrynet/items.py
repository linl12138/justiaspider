# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IndustrynetItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    physical_address = scrapy.Field()
    mailing_address = scrapy.Field()
    phone = scrapy.Field()
    name = scrapy.Field()
    capabilities = scrapy.Field()
    brands = scrapy.Field()
    sic = scrapy.Field()
    pass

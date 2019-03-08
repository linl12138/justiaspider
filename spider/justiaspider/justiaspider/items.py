# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field

class JustiaItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    country = Field()
    title = Field()
    plaintiff = Field()
    defendant = Field()
    case_num = Field()
    filed = Field()
    court = Field()
    Presiding_Judge = Field()
    nature_suit = Field()
    cause_action = Field()
    jury_demanded = Field()




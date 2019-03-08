# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#from scrapy.spider import spider

import json
from justiaspider.items import *

class JustiaJsonfilePipeline(object):
    
    def __init__(self):
        pass
    
    
    def process_item(self,item,spider):
        data=dict(item)
        with open ('just.json','a',encoding='utf-8')as f:
            f.write(json.dumps(data,ensure_ascii=True))



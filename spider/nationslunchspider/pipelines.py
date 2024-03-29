# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json



class CustomPipeline(object):

    def open_spider(self, spider):
        if spider.name == 'Nationsspider':
            self.file = open('c:/Users/Markus/desktop/projects/nationslunch/spider/nationslunchspider/output/images.jl', 'w')
            self.file.truncate()
    
        if spider.name == 'gspider':
            self.file = open('../output/phone.jl','w')
            self.file.truncate()

       
    def close_spider(self,spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

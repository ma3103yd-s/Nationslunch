# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NationslunchspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    #date = scrapy.Field()
    file_urls = scrapy.Field()
    date = scrapy.Field()
    #files = scrapy.Field()

class GSpiderItem(scrapy.Item):

    phone_nbr = scrapy.Field()

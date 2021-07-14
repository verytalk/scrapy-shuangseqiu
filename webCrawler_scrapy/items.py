# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class WebcrawlerScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    openDate = scrapy.Field()
    issueDate = scrapy.Field()
    issueNo_1 = scrapy.Field()
    issueNo_2 = scrapy.Field()
    issueNo_3 = scrapy.Field()
    issueNo_4 = scrapy.Field()
    issueNo_5 = scrapy.Field()
    issueNo_6 = scrapy.Field()
    issueNo_blue = scrapy.Field()
    issueAmountTotal = scrapy.Field()
    firstPrize = scrapy.Field()
    secondPrize = scrapy.Field()
    remark = scrapy.Field()


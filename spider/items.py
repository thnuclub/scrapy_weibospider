# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TweetItem(scrapy.Item):
    verified = scrapy.Field()
    name = scrapy.Field()
    keyword = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()
    pic = scrapy.Field()
    source = scrapy.Field()
    cdate = scrapy.Field()
    retweet = scrapy.Field()
    headurl = scrapy.Field()

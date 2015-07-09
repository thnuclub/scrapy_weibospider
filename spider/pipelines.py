# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from elasticsearch import Elasticsearch
import hashlib
import settings

class SpiderPipeline(object):
    def __init__(self):
        self.es = Elasticsearch(settings.ES_HOST)

    def process_item(self, item, spider):
        print 'md5 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        str = item['url']
        if item['retweet']:
            if item['retweet']['url']:
                str += item['retweet']['url']
        md5 = hashlib.md5(str).hexdigest()
        self.es.index(index="weibo", doc_type="tweet", id=md5, body=item)
        return item

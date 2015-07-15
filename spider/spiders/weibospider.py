#coding=utf8
import scrapy
import requests
import redis
from scrapy import signals
from scrapy.http import Request
from spider.sina.weibo import weibo
from spider.items import TweetItem
from scrapy.exceptions import DontCloseSpider
import spider.sina.parser as parser
from scrapy import log
import time

class WeiboSpider(scrapy.Spider):
    name = "weibospider"

    def __init__(self, name, password, *args, **kwargs):
        self.weibo = weibo(name, password)
        self.session = self.weibo.login()
        cookiejar = requests.utils.dict_from_cookiejar(self.session.cookies)

        self.cookie = {'ALF': cookiejar['ALF'],
                       'SUB': cookiejar['SUB'],
                       'SUBP': cookiejar['SUBP'],
                       'SUE': cookiejar['SUE'],
                       'SUHB': cookiejar['SUHB'],
                       'SUP': cookiejar['SUP'],
                       'SUS': cookiejar['SUS']}
        print self.cookie

    def _set_crawler(self, crawler):
        super(WeiboSpider, self)._set_crawler(crawler)
        self.setup_redis()

    def setup_redis(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379)
        self.crawler.signals.connect(self._on_idle, signal=signals.spider_idle)
        self.crawler.signals.connect(self.item_scraped, signal=signals.item_scraped)

    def item_scraped(self, *args, **kwargs):
        self._on_idle()

    def _on_idle(self, spider):
        for i in range(0, 10):
            url = self.redis_client.lpop("weibospider:urls")
            log.msg('from redis.list read %s' % url, log.INFO)
            if url:
              self.crawler.engine.crawl(Request(url=url, cookies=self.cookie, callback=self._parse, errback=self._parse_fail), spider=self)
            else:
              break
        raise DontCloseSpider

    def start_requests(self):
        utctime = int(time.time())
        url = 'http://d.weibo.com/102803?topnav=1&mod=logo&wvr=6&%s'%(utctime)
        yield Request(url=url, cookies=self.cookie, callback=self._parse, errback=self._parse_fail)

    def _parse(self, response):
        tweets,hrefs = parser.parse_html(response.body)
        for tweet in tweets:
            item = TweetItem()
            item = tweet
            yield item
        
        for href in hrefs:
            yield Request(url=href, cookies=self.cookie, callback=self._parse, errback=self._parse_fail)

    def _parse_fail(self, response):
        log.err("Fail to parse the http response file.")

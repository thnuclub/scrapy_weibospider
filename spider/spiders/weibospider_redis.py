from scrapy_redis.spiders import RedisSpider
from spider.sina.weibo import weibo
from scrapy.http import Request
from spider.items import TweetItem
from scrapy import log
import spider.sina.parser as parser
import requests

class WeiboSpiderRedis(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'weibospider'
    redis_key = 'weibospider:start_urls'

    def __init__(self, name, password, *args, **kwargs):
        self.weibo = weibo(name, password)
        self.session = self.weibo.login()
        super(WeiboSpiderRedis, self).__init__(*args, **kwargs)
        cookiejar = requests.utils.dict_from_cookiejar(self.session.cookies)

        self.cookie = {'ALF': cookiejar['ALF'],
                       'SUB': cookiejar['SUB'],
                       'SUBP': cookiejar['SUBP'],
                       'SUE': cookiejar['SUE'],
                       'SUHB': cookiejar['SUHB'],
                       'SUP': cookiejar['SUP'],
                       'SUS': cookiejar['SUS']}

    def make_requests_from_url(self, url):
        return Request(url=url, cookies=self.cookie, callback=self.parse, errback=self.parse_fail)

    def parse(self, response):
        tweets,hrefs = parser.parse_html(response.body)
        for tweet in tweets:
            item = TweetItem()
            item = tweet
            yield item
        for href in hrefs:
            yield Request(url=href, cookies=self.cookie, callback=self._parse, errback=self._parse_fail)

    def parse_fail(self, response):
        log.err("Fail to parse the http response file.")


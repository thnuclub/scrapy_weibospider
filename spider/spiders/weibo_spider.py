#coding=utf8
import scrapy
import requests
from scrapy.http import Request
from spider.sina.weibo import weibo
from spider.items import TweetItem
import spider.sina.parser as parser
from scrapy import log

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
        
    def start_requests(self):
        home_url = 'http://s.weibo.com/weibo/%25E6%259F%25AF%25E9%259C%2587%25E4%25B8%259C&Refer=STopic_top'
        yield Request(url=home_url, cookies=self.cookie, callback=self._parse, errback=self._parse_fail)

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


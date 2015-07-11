# -*-coding:utf-8-*-

import time
import requests
import urllib
import sys
from bs4 import BeautifulSoup
import redis
reload(sys)
sys.setdefaultencoding('utf-8')

redisClient=redis.StrictRedis(host='127.0.0.1',port=6379)
redis_key = 'weibospider:start_urls'

def get_html_and_parse():
    url = u'http://s.weibo.com/top/summary?cate=realtimehot'
    print url
    req = requests.get(url,cookies = cookie, timeout=100)
    lines = req.text.splitlines()
    for line in lines:
        if line.startswith('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_top_realtimehot"'):
            n = line.find('html":"')
            if n > 0:
                html = line[n + 7: -12].encode("utf-8").decode('unicode_escape').encode("utf-8").replace("\\", "")
                if html.find('<p class="star_name">') > 0:
                    soup = BeautifulSoup(html)
                    dls = soup.find_all('p', attrs={'class': 'star_name'})
                    for dl in dls:
                        try:
                            word = dl.find('a').text.strip()
                            utctime = int(time.time())
                            url = u"http://s.weibo.com/weibo/%s?topnav=1&wvr=6&topsug=1&%s" % (urllib.quote_plus(word.encode('utf-8')), utctime)
                            redisClient.rpush(redis_key, url)
                            print time.time(), word, url
                        except Exception, e:
                            print 'parse tweet error', e

if __name__ == "__main__":
    login = False
    cookie = ""
    while True:
        try:
            get_html_and_parse()
            time.sleep(15*60)
        except Exception , e:
            print 'parse html', e
            time.sleep(60)

# -*-coding:utf-8-*-

from bs4 import BeautifulSoup
import time
import urlparse
import urllib

format = '%Y-%m-%d %H:%M:%S'

def get_tweet(dl):
    tweet = {}
    tweet['retweet'] = {}
    tweet['source'] = {}
    tweet['pic'] = ""
    tweet['verified'] = False
    tweet['text'] = dl.find('p', attrs={'node-type': 'feed_list_content'}).text.strip()
    
    o = dl.find('img', attrs={'class': 'W_face_radius'}).attrs
    tweet['headurl'] = o['src']
    tweet['name'] = o['alt']

    info = dl.select('div.feed_content > a')
    if len(info) >=2:
        if info[1].attrs.has_key('class'):
            if 'approve' in info[1].attrs['class']:
                tweet['verified'] = True
            if 'approve_co' in info[1].attrs['class']:
                tweet['verified'] = True
    pics = dl.findAll('img', attrs={'action-type': 'feed_list_media_img'})
    for pic in pics:
        tweet['pic'] += pic.attrs['src'] + ","
    
    o = dl.select('div.feed_from > a')
    date = o[0].attrs
    tweet['cdate'] = time.strftime(format,time.localtime(int(date['date'])/1000))
    tweet['url'] = date['href']
    source = o[1]
    tweet['source']['name'] =  source.text
    tweet['source']['url'] =  source.attrs['href']
    return tweet

def get_retweet(dl):
    retweet = {}
    comment = dl.select('div.comment > div.comment_info')
    if len(comment) > 0:
        u = comment[0].select('div > a')
        if len(u) > 0:
            if u[0].attrs.has_key('title'):
                retweet['name'] = u[0].attrs['title']
            if u[0].attrs.has_key('usercard'):
                retweet['uid'] = u[0].attrs['usercard'][3:-1]
                retweet['text'] = comment[0].find('p', attrs={'class': 'comment_txt'}).text
        if len(u) > 1:
            retweet['verified'] = False
            if u[1].attrs.has_key('class'):
                if 'approve' in u[1].attrs['class']:
                    retweet['verified'] = True
                if 'approve_co' in u[1].attrs['class']:
                    retweet['verified'] = True

        pics = comment[0].findAll('img')
        retweet['pic'] = ''
        for pic in pics:
            retweet['pic'] += pic.attrs['src'] + ","
        
    comment = dl.select('div.comment > div.comment_info')
    if comment  and len(comment) > 0:
        cc = comment[0].find('div', attrs={'class': 'feed_from'})
        cc = cc.findAll('a')
        if len(cc) > 0:
            date = cc[0].attrs
            retweet['cdate'] = time.strftime(format,time.localtime(int(date['date'])/1000))
            retweet['url'] = date['href']
        if len(cc) > 1:
            source = cc[1]
            retweet['source'] = {}
            retweet['source']['name'] =  source.text
            retweet['source']['url'] =  source.attrs['href']
    return retweet

def parse_html(text):
    lines = text.splitlines()
    isCaught = True
    hasMore = True
    tweets = []
    next_hrefs = []
    for line in lines:
        if line.startswith('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_weibo_direct"'):
            isCaught = False
            n = line.find('html":"')
            if n > 0:
                html = line[n + 7: -12].encode("utf-8").decode('unicode_escape').encode("utf-8").replace("\\", "")
                if html.find('<div class="search_noresult">') > 0:
                    hasMore = False
                else:
                    soup = BeautifulSoup(html)
                    dls = soup.find_all('div', attrs={'class': 'feed_list'})
                    for dl in dls:
                        try:
                            tweet = get_tweet(dl)
                            tweet['retweet'] = get_retweet(dl)
                            tweets.append(tweet)
                        except Exception , e:
                            print 'parse tweet error', e
                    href = get_nextpage(soup)
                    if href:
                        next_hrefs.append(href)
    if isCaught:
        print '被新浪识别为机器人,请手动登陆账号检查!'
        return [], []
    if not hasMore:
        print 'Not More Results'
        return [], []
    return tweets, next_hrefs

def get_nextpage(soup):
    pages = soup.find('div', attrs={'class': 'W_pages'})
    if pages is None or len(list(pages.find_all('a'))) == 0:
        return None
    else:
        next_page = pages.find_all('a')[-1]
        if next_page.text.strip() == u'下一页':
            next_href = next_page['href']
            if not next_href.startswith('http://'):
                next_href = urlparse.urljoin('http://s.weibo.com', next_href)
                url, query = tuple(next_href.split('&', 1))
                base, key = tuple(url.rsplit('/', 1))
                key = urllib.unquote(key)
                url = '/'.join((base, key))
                next_href = '&'.join((url, query))
                return next_href
    return None

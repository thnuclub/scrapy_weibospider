# -*-coding:utf-8-*-

# -*- coding: utf-8 -*-
import urllib
import urllib2
import requests
import base64
import json
import binascii
import cookielib

import rsa
import re

publickey='EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB\
784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'
pubkey=int(publickey,16)

class weibo:
    user_agent = (
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) '
        'Chrome/20.0.1132.57 Safari/536.11'
    )
    session = requests.session()
    session.headers['User-Agent'] = user_agent

    def __init__(self, username, pwd):
        self.username = username
        self.password = pwd
        # Get a Cookie object
        self.cookie_obj = cookielib.LWPCookieJar()
        # Bind Cookie object to HttpRequest Object
        self.cookie_support = urllib2.HTTPCookieProcessor(self.cookie_obj)
        # Init an opener
        self.opener = urllib2.build_opener(self.cookie_support, urllib2.HTTPHandler)
        # Install the opener object
        urllib2.install_opener(self.opener)

    def b64(self, sth):
        return base64.b64encode(sth.encode()).decode('utf-8')

    def get_su(self):
        string=urllib.quote(self.username)
        return self.b64(string)

    def get_sp(self, st,nc):
        key=rsa.PublicKey(pubkey,65537)
        message=str(st)+'\t'+str(nc)+'\n'+self.password
        sp=rsa.encrypt(message.encode(),key)
        sp=binascii.b2a_hex(sp)
        return sp.decode('utf-8')

    def get_servertime(self):#and nonce

        url='http://login.sina.com.cn/sso/prelogin.php?entry=weibo&su=%s&checkpin=1&rsakt=mod' %(self.get_su())
        page=self.opener.open(url)
        data=json.loads(page.read().decode('utf-8'))
        
        result=[]
        result.append(str(data['servertime']))
        result.append(str(data['nonce']))
        result.append(str(data['pcid']))
        return result

    def login(self):
        result = self.get_servertime()
        servertime = result[0]
        nonce= result[1]
        postdata={
            'entry':'weibo',
            'gateway':'1',
            'from':'',
            'savestate':'7',
            'useticket':'1',
            #'pagerefer':'http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F',
            'vsnf':'1',
            'su':'',
            'service':'miniblog',
            'servertime':'',
            'nonce':'',
            'pwencode':'rsa2',
            'rsakv':'1330428213',
            'sp':'',
            'sr':'1280*800',
            'encoding':'UTF-8',
            'prelt':'34',
            'url':'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype':'META'
        }
        postdata['su']= self.get_su()
        postdata['sp']= self.get_sp(servertime,nonce)
        postdata['servertime'] = servertime
        postdata['nonce'] = nonce

        url='http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36 OPR/27.0.1689.66 (Edition Baidu)',
        }
        data = urllib.urlencode(postdata)
        req_login  = urllib2.Request(
            url,data,
            headers
        )
        resp = urllib2.urlopen(req_login)
        text = resp.read()
        login_url = re.search(r'replace\([\"\']([^\'\"]+)[\"\']', text).group(1)
        self.session.get(login_url)
        self.session.get('http://weibo.com')
        return self.session

if __name__ == '__main__':
    pass
    #weibo = weibo('qpf_2008@163.com', '983436938')
    #weibo.login('qpf_2008@163.com', '983436938')

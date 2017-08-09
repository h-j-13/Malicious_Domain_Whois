# !/usr/bin/python
# encoding:utf-8
"""
    CN域名获取

func  : 从域名交易网站中获取域名
author: @`13

version     : 0.1.0
last-update :2016.10.5
"""

import urllib
import urllib2
from random import choice

from MyLib_py.Func_lib import timelimited


class spider:
    """爬虫类"""

    def __init__(self, url=None):
        """
        :param url: 基础链接
        """
        self.baseURL = url

    @staticmethod
    # @timelimited(TimeOut)
    def getPageText(url, timeOut=5, useHaeder=False, reSetHaeder=False, ):
        """
        获取页面内容
        :param url: URL
        :param timeOut:超时设置
        :param useHaeder: 使用头部标志
        :param reSetHaeder: 重设头部标志
        :return: url的内容
        """

        # 头部信息 浏览器标示集合
        USER_AGENTS = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        ]

        # 火狐（Firefox）标准Linux头部信息
        send_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive'
        }

        send_headers_ = {
            "Accept":"application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Connection":"keep-alive",
            "Content-Length":"186",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie":"ASP.NET_SessionId=kfxwu5gprbgwz2c3iqo1f5hq; CNZZDATA906087=cnzz_eid%3D110864443-1476061789-http%253A%252F%252Fwww.22.cn%252F%26ntime%3D1476081501; Hm_lvt_c37800fabdf21cf4f786cb0d5f794f12=1476066792,1476068646; Hm_lpvt_c37800fabdf21cf4f786cb0d5f794f12=1476084856",
            "Host":"am.22.cn,",
            "Origin":"https://am.22.cn,",
            "Referer":"https://am.22.cn/ykj/?t=0.20652880301847176&ddlSuf=.cn&registrar=0&chkorder=-1&chkday=-1&position=&position1=&position2=&MinPrice=0&MaxPrice=&selMinLen=&selMaxLen=&dealtype=2&keytype=0&issch=1&showtype=0",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest"
        }
        # 重设头部
        if reSetHaeder:
            send_headers['User-Agent'] = choice(USER_AGENTS)
            # print send_headers['User-Agent']

        # 使用头部
        if useHaeder:
            req = urllib2.Request(url, headers=send_headers_)
            try:
                response = urllib2.urlopen(req, timeout=timeOut)
            except Exception as errorMassage:
                print errorMassage
                print "[urllib2_Error]解析" + str(url) + "内容失败！"
                return None
            return response.read()
        # 不使用头部（简单urllib打开
        else:
            try:
                text = urllib.urlopen(url).read()
            except Exception as errorMassage:
                print errorMassage
                print "[urllib_Error]解析" + str(url) + "内容失败！"
                return None
            return text

#!/usr/bin/python
# encoding:utf-8

#
# CN域名获取
# func  : 易名网获取域名信息
# time  : 2016.10.5
# author: @`13
#

import re
import time

from CN_spider_main import spider
from MyLib_py.Func_lib import timelimited


#  易名网 cn域名交易基础页面
YIMING_BASIC_URL = 'http://auction.ename.com/tao/buynow?domaintld%5B0%5D=2&transtype=0&sort=1&page='
PAGE_NUM = 4293  # 需要爬取的页面数量


class YIMING_spider(spider):
    def __init__(self,):
        spider.__init__(self, YIMING_BASIC_URL)

    def __getUrl(self, pagenum=1):
        """合成网页url"""
        return YIMING_BASE_URL+str(pagenum)

    def getDomainInfo(self, timeInterval=3):
        """
        获取网页信息
        :param timeInterval:时间间隔
        :return:
        """
        for num in range(1, PAGE_NUM+1):
            url = self.__getUrl(num)
            HTML_text = None
            while HTML_text is None:
                HTML_text = self.getPageText(url, useHaeder=True, reSetHaeder=True)
                time.sleep(timeInterval)
            # print HTML_text
            pattern = re.compile(r'(<span>.*cn</span>)')
            for match in pattern.findall(HTML_text):
                print match[6:-7]



if __name__ == '__main__':
    # 重定向输出到一个文件中即可
    YM = YIMING_spider()
    YM.getDomainInfo()

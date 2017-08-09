#!/usr/bin/python
# encoding:utf-8

#
# CN域名获取
# func  : 爱名网获取域名信息
# time  : 2016.10.10
# author: @`13
#

import re
import time

from CN_spider_main import spider
from MyLib_py.Func_lib import timelimited

AIMING_BasicUrl = 'https://am.22.cn/ajax/yikoujia/default.ashx?t=0.0013572423563918967'

class YIMING_spider(spider):
    def __init__(self,):
        spider.__init__(self, AIMING_BasicUrl)

    def __getUrl(self, pagenum=1):
        """合成网页url"""
        return AIMING_BasicUrl+str(pagenum)

    def getDomainInfo(self, timeInterval=3):
        """
        获取网页信息
        :param timeInterval:时间间隔
        :return:
        """
        for num in range(1, 2):
            url = AIMING_BasicUrl
            HTML_text = None
            while HTML_text is None:
                HTML_text = self.getPageText(url, useHaeder=True, reSetHaeder=True)
                time.sleep(timeInterval)
            # print HTML_text
            pattern = re.compile(r'(>*.?cn</a>)')
            for match in pattern.findall(HTML_text):
                print match[6:-7]


if __name__ == '__main__':
    # 重定向输出到一个文件中即可
    YM = YIMING_spider()
    YM.getDomainInfo()

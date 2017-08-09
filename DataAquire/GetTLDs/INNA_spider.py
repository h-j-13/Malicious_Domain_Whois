#!/usr/bin/python
# encoding:utf-8

#
# WhoisSrv获取-来自INNA
# func  : 从INNA获取TLD及其whois_srv的信息
# time  : 2016.9.12
# author: @`13
#

import re
import time
import urllib
import urllib2
import sys

INNA_url = 'http://www.iana.org/domains/root/db'    # INNA 的 TLD数据页面
# TLD 信息字典
TLD_info = {'TLD': '',       # TLD
            'link': '',      # 连接
            'punycode': '',  # Punycode码
            'type': '',      # 类型
            'WhoisSrv': '',  # Whois服务器
            'SponsoringOrganisation': ''}   # 注册组织


class spider:
    """INNA 爬虫类"""
    def __init__(self):
        self.url = INNA_url

    @staticmethod
    def getPageText(url):
        """获取页面内容
        :return url的HTML源码"""
        try:
            text = urllib.urlopen(url).read()
        except:
            print "[Error]解析"+str(url)+"内容失败！"
            return "No data"
        return text

    @staticmethod
    def getTLDinfo(html, intervalsTime=3):
        """从html源码中获取TLD有关信息
        :param @html html源码
        :return TLD信息字典"""
        # 匹配内容
        pattern = re.compile(r'(<span class="domain tld"><a href=".*?">[\s\S]*?</tr>)')
        for match in pattern.findall(html):
            #  print match
            TLDinfo = TLD_info  # 初始化一个新的TLD信息字典
            pattern2 = re.compile(r'(a href=".*?".*?<|<td>.*?</td>[\s\S]*?<td>.*?</td>)')
            for match2 in pattern2.findall(match):
                if match2.find("a href=") != -1:
                    TLDinfo['TLD'] = str(match2.split('>')[1][:-1]).lower()
                    if TLDinfo['TLD'].find("&#x200f;") != -1:   # 处理特殊的字符
                        #  print '[ Test ]'+TLDinfo['TLD'].strip("&#x200f;").strip("&#x200e;").strip()
                        TLDinfo['TLD'] = TLDinfo['TLD'].strip("&#x200f;").strip("&#x200e;").strip()
                    TLDinfo['link'] = 'http://www.iana.org' + match2.split('"')[1].strip()
                    if TLDinfo['link'].find("xn--") != -1:  # 获取punycode
                        TLDinfo['punycode'] = match2.split('"')[1].strip().split('/')[-1].strip('.html')
                    else:
                        TLDinfo['punycode'] = TLDinfo['TLD'].strip('.').strip()
                elif match2.find("<td>") != -1:
                    TLDinfo['type'] = match2.split('</td>')[0].strip('<td>').strip()
                    TLDinfo['SponsoringOrganisation'] = match2.split('</td>')[1].strip().strip('<td>').strip()
            # TLDinfo = spider.getTLDWhoisSrv(**TLDinfo)
            yield TLDinfo   # 转化成一个生成器
            time.sleep(intervalsTime)   # 防Ban

    @staticmethod
    def getTLDWhoisSrv(**TLDinfo):
        """获取TLD详细页面中的Whois_srv
        :param @TLDinfo TLD信息字典
        :return 获取了WhoisSrv内容的信息字典"""
        Text = spider.getPageText(TLDinfo['link'])
        # 提取WhoisSrv
        pattern = re.compile(r'(WHOIS Server:.*)')
        for match in pattern.findall(Text):
            TLDinfo['WhoisSrv'] = match.split('</b>')[1].strip()
        return TLDinfo

if __name__ == '__main__':
    count = 0
    IS = spider()
    for item in IS.getTLDinfo(IS.getPageText('http://www.iana.org/domains/root/db')):
        IS.getTLDWhoisSrv(**item)
        count += 1
        if count == 2:
            print item
            break


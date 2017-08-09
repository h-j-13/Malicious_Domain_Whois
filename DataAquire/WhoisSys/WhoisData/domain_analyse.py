#!/usr/bin/env python
# encoding:utf-8

"""
    域名处理,分解与编码
==========================

version   :   1.0
author    :   @`13
time      :   2017.1.18
"""

import sys
import tldextract

reload(sys)
sys.setdefaultencoding('utf8')


class DomainAnalyse:
    """域名分析模块"""
    def __init__(self, raw_domain):
        """初始化"""
        raw_domain = raw_domain.lower()  # 转换小写

        # 一次过滤无效的的域名信息，如'/'后的内容
        result = tldextract.extract(raw_domain)
        raw_domain = ''
        if result.subdomain != '':
            raw_domain = result.subdomain
        if result.domain != '':
            raw_domain = raw_domain + '.' + result.domain
        if result.suffix != '':
            raw_domain = raw_domain + '.' + result.suffix
        raw_domain = raw_domain.strip('.')

        after_domain = ''
        i = 0
        for domain_part in raw_domain.split("."):
            if i != 0:
                after_domain += '.'
            domain_part_temp = domain_part
            while domain_part_temp.find('-') != -1:
                domain_part_temp = domain_part_temp.replace('-', '')

            if not domain_part_temp.isalnum():
                domain_part = self.to_punycode(domain_part)

            after_domain += domain_part
            i = 1

        result = tldextract.extract(after_domain)
        self.subdomain = result.subdomain  # 子域名
        self.domain = result.domain  # 主机名
        self.domain_suffix = result.suffix  # 后缀


    def get_tld(self):
        """:return 获得查询顶级域名（whois服务器数据库查询域名,utf8）"""
        if self.domain_suffix == "web.za" or self.domain_suffix == "co.za" or \
                        self.domain_suffix == "net.za" or self.domain_suffix == "web.za":
            return self.domain_suffix
        else:
            if self.domain_suffix.find("xn--") != -1:
                self.domain_suffix = self.to_utf8(self.domain_suffix)
            suffix_split = self.domain_suffix.split(".")
            return suffix_split[-1]

    def get_punycode_tld(self):
        """:return Punycode格式TLD"""
        return self.domain_suffix.split('.')[-1]

    def get_utf8_domain(self):
        """:return uft_8格式域名"""
        domain = self.domain
        domain_suffix = self.domain_suffix
        if self.domain.find("xn--") != -1:
            domain = self.to_utf8(domain)
        if self.domain_suffix.find("xn--") != -1:
            domain_suffix = self.to_utf8(domain_suffix)
        return (domain + "." + domain_suffix).strip('.')

    def get_punycode_domain(self):
        """:return Punycode格式域名"""
        return (self.domain + "." + self.domain_suffix).strip('.')

    def to_punycode(self, nonEnglishDomain):
        """
        :param nonEnglishDomain: 非英文域名
        :return: Punycode格式域名
        """
        return 'xn--' + str(nonEnglishDomain).decode('utf8').encode('punycode')

    # punycode 转换为utf8编码
    def to_utf8(self, punycodeDomain):
        """
        :param punycodeDomain: Punycode格式域名
        :return: uft_8格式域名
        """
        return str(punycodeDomain).replace('xn--', '').decode('punycode').encode('utf8')

    @classmethod
    def get_punycode(cls, string):
        """:return: Punycode格式全域名"""
        string = string.split('.')[1]
        if not str(string).isalnum():
            return 'xn--' + str(string).decode('utf8').encode('punycode')
        else:
            return str(string)


if __name__ == '__main__':
    # Demo
    raw_domain = '00000.slsqqhz.net'
    an = DomainAnalyse(raw_domain)
    print 'raw_domain           :', raw_domain
    print 'domain               :', an.get_utf8_domain()
    print 'domain_punycode      :', an.get_punycode_domain()
    print 'tld_punycode         :', an.get_punycode_tld()

    domains = ['xn--3e0b707e',
               'xn--90a3ac',
               'xn--clchc0ea0b2g2a9gcd',
               'xn--fiqs8s',
               'xn--fiqz9s',
               'xn--fzc2c9e2c',
               'xn--j1amh',
               'xn--j6w193g',
               'xn--kpry57d',
               'xn--lgbbat1ad8j',
               'xn--mgbaam7a8h',
               'xn--mgberp4a5d4ar',
               'xn--o3cw4h',
               'xn--ogbpf8fl',
               'xn--p1ai',
               'xn--pgbs0dh',
               'xn--wgbh1c',
               'xn--wgbl6a',
               'xn--xkc2al3hye2a',
               'xn--yfro4i67o']

    for domain in domains:
        an = DomainAnalyse(domain)
        print an.get_punycode_domain()

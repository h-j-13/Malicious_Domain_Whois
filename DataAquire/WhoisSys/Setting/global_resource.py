#!/usr/bin/env python
# encoding:utf8

"""
    公共资源
===============

version   :   1.0
author    :   @`13
time      :   2016.11.5
"""

from WhoisConnect.server_ip import ServerIP
from WhoisConnect.whois_tld import TLD
from WhoisData.get_whois_func import Func
from WhoisData.domain_analyse import DomainAnalyse

class Resource(object):
    """公共资源类"""
    # Global Class
    WhoisSrv = None     # whois服务器ip查询
    TLD = None          # TLD whois映射关系查询
    Domain = None       # 域名分析
    WhoisFunc = None    # whois服务器提取函数查询

    # Singleton
    _instance = None

    def __new__(cls, *args, **kw):
        """单例模式"""
        if not cls._instance:
            cls._instance = super(Resource, cls).__new__(cls, *args, **kw)
        return cls._instance

    # 初始化域名信息相关
    @staticmethod
    def global_object_init():
        Resource.WhoisSrv = ServerIP()  # whois服务器ip查询
        Resource.TLD = TLD()  # TLD whois映射关系查询
        Resource.Domain = DomainAnalyse  # 域名分析
        Resource.WhoisFunc = Func()  # whois服务器提取函数查询

if __name__ == '__main__':
    # Demo
    Resource.global_object_init()

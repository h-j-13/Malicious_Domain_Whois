#!/usr/bin/env python
# encoding:utf-8

"""
Whois 连接模块
获取连接所需数据,与whois服务器通信获取whois信息
"""

__version = '2017.1.15'


class Info(object):
    """whois连接基础信息"""
    # Singleton
    _instance = None

    def __new__(cls, *args, **kw):
        """单例模式"""
        if not cls._instance:
            cls._instance = super(Info, cls).__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        """初始化数据"""
        pass

    def get_info(self, agrvs=''):
        """通过参数获取链接所需要的数据"""
        pass

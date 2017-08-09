#!/usr/bin/env python
# encoding:utf-8

"""
    获取whois服务器对应的提取函数
==================================

version   :   1.0
author    :   @`13
time      :   2017.1.19
"""

from Setting.static import Static
Static.static_value_init()


class Func(object):
    """获取whois服务器对应的提取函数"""

    # Singleton
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Func, cls).__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        """数据初始化"""
        self.server_func_dict = {}
        WhoisServiceFuncFile = open(Static.WHOIS_FUNC_FILE, 'r')
        for line in WhoisServiceFuncFile.readlines():
            if line.find('#') != -1:
                pass
            if line.find(':') != -1:
                key = line.split(':')[0].strip()
                value = line.split(':')[1].strip()
                self.server_func_dict.setdefault(key, value)
        WhoisServiceFuncFile.close()

    def get_whois_func(self, whois):
        """
        获取whois对应的提取函数名称
        :param whois: whois服务器
        :return: 对应的提取函数名称 (找不到则默认返回通用提取函数 general_manage)
        """
        result = self.server_func_dict.get(whois, [])
        return 'general_manage' if not result else result


if __name__ == '__main__':
    # Demo
    W = Func()
    S = Func()
    print id(W)
    print id(S)
    print S.get_whois_func('whois.crsnic.net')
    print W.get_whois_func('whois.nic.pw')
    print W.get_whois_func('whois.nic.party')
    print W.get_whois_func('whois.cnnic.cn')
    print W.get_whois_func('whois.example.13')

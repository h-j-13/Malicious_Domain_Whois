#!/usr/bin/env python
# encoding:utf-8

"""
    whois服务器与TLD映射关系
=============================

version   :   1.0
author    :   @`13
time      :   2017.1.18
"""
from random import choice

from __init__ import Info
from Setting.static import Static
from Database.db_opreation import DataBase
from Database.SQL_generate import SQL_generate

Static.static_value_init()


class TLD(Info):
    """获取TLD对应的whois服务器"""
    def __init__(self):
        """数据初始化"""
        server_addr_dict = {}
        MySQL = DataBase()
        MySQL.db_connect()
        SQL = SQL_generate.TLD_WHOIS_ADDR_INFO(Static.WHOIS_TLD_TABLE)
        results = MySQL.execute(SQL)
        for result in results:
            key = result[0]
            if not result[1]:   # 删除无记录的whois数据
                continue
            values = result[1].split(',')
            server_addr_dict.setdefault(key, values)
        self.server_addr_dict = server_addr_dict
        MySQL.db_close()

    def get_server_addr(self, tld):
        """
        获取tld对应的whois服务器(有多个则随机选择一个)
        :param tld: tld
        :return: 对应的whois服务器
        """
        result = self.server_addr_dict.get(tld, [])
        return None if not result else choice(result)


if __name__ == '__main__':
    tld = TLD()
    T = TLD()
    print id(tld)
    print id(T)
    for i in xrange(3):
        print T.get_server_addr('cn')
    for i in xrange(3):
        print tld.get_server_addr('info')
    print str(tld.get_server_addr('tld_example'))
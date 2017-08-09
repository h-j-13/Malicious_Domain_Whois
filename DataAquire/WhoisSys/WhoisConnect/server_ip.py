#!/usr/bin/env python
# encoding:utf-8

"""
    获取whois服务器的IP地址
=============================

version   :   1.0
author    :   @`13
time      :   2017.1.17
"""

import time
from random import choice

from __init__ import Info
from Database.db_opreation import DataBase
from Database.SQL_generate import SQL_generate
from Setting.static import Static


Static.static_value_init()


class ServerIP(Info):
    """whois服务器IP"""
    def __init__(self):
        self.dictProtect = True     # 数据字典保护锁
        self.__whoisAddrDictInit()
        self.dictProtect = False

    def __whoisAddrDictInit(self):
        """whois服务器ip字典数据初始化"""
        DB = DataBase()
        DB.db_connect()
        whois_ip_dict = {}
        GET_WHOIS_ADDR_SQL = SQL_generate.WHOIS_SRV_INFO(Static.SRVIP_TABLE)
        results = DB.execute(GET_WHOIS_ADDR_SQL)
        # 将whois服务器ip数据读入内存(字典)中
        for result in results:
            key = result[0]
            if not result[1]:
                continue
            ip_list = result[1].split(',')
            values = []
            if result[2]:
                port_available_list = list(result[2])
                for i, ip in enumerate(ip_list):
                    if port_available_list[i] == '1':
                        values.append(ip)
            whois_ip_dict.setdefault(key, values)
        DB.db_close()
        self.whois_ip_dict = whois_ip_dict

    def get_server_ip(self, server_addr):
        """
        获取whois服务器的ip地址
        :param server_addr: whois服务器名称 (需全小写,例如 : whois.cnnic.cn)
        :return: 该服务器对应的一个随机ip,无记录则默认返回 None
        """
        while self.dictProtect:
            time.sleep(0.1)
        result = self.whois_ip_dict.get(server_addr, [])
        return None if not result else choice(result)
        

if __name__ == '__main__':
    # Demo
    WhoisServerIP = ServerIP()
    single = ServerIP()
    print id(WhoisServerIP)
    print id(single)
    for i in xrange(5):
        print WhoisServerIP.get_server_ip('whois.verisign-grs.com')
    for i in xrange(5):
        print str(single.get_server_ip('abc'))


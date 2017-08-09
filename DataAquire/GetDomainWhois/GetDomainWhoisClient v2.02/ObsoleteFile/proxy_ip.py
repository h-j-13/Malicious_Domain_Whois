#!/usr/bin/python
# encoding:utf-8

# 获取代理ip
# @author wangkai
# @version 1.0
# 2015.12.10


import datetime
import time
from threading import Lock, Thread
from random import choice
from db_operation import DataBase


class ProxyIP:
    def __init__(self):
        self.db = DataBase()
        self.__ip_refresh()
        self.proxy_ip_dict = {}

    # 代理IP刷新
    def __ip_refresh(self):
        self.sign_refresh = 0  # 刷新标志
        print str(datetime.datetime.now()).split(".")[0], '代理IP刷新'
        self.db.connect()
        self.init_data = self.db.get_proxy_ip()  # 初始数据库读取内容
        self.db.close()
        self.__ip_synthesis()  # 代理IP表

    # IP与端口合成代理IP列表
    def __ip_synthesis(self):
        self.proxy_ip_dict = {}
        if self.init_data != None:
            for result in self.init_data:
                whois_server_ip = result.whois_server_ip
                one_proxy_ip = OneProxyIP(result.ip, result.port, result.mode)
                if self.proxy_ip_dict.get(whois_server_ip, None) is not None:
                    self.proxy_ip_dict[whois_server_ip].append(one_proxy_ip)
                else:
                    list_temp = []
                    list_temp.append(one_proxy_ip)
                    self.proxy_ip_dict.setdefault(whois_server_ip, list_temp)

    # 根据whois服务器ip随机获取一个代理IP
    # gevent模式, 不用考虑多线程冲突
    # @return (ip, port, mode)
    def get_proxy_ip(self, whois_server_ip):
        if self.sign_refresh > 100000: # 获取10万刷新一次
            self.__ip_refresh()
        proxy_ip_list = self.proxy_ip_dict.get(whois_server_ip, None)
        if proxy_ip_list is not None:
            return choice(proxy_ip_list)
        else:
            return None

# 一条proxy记录
class OneProxyIP:
    ip = ""
    port = 0
    mode = 4
    def __init__(self, ip, port, mode):
        self.ip = ip
        self.port = port
        self.mode = mode

if __name__ == '__main__':
    proxy_ip = ProxyIP()
    for i in range(10):
        print proxy_ip.get_proxy_ip()

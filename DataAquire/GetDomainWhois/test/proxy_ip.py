#!/usr/bin/python
# encoding:utf-8

# 获取代理ip
# @author wangkai
# @version 1.0
# 2015.12.10

from random import choice

import static

logger = static.logger


class ProxyIP:
    def __init__(self):
        self.DB = static.newDB()
        self.__ip_refresh()

    # 代理IP刷新
    def __ip_refresh(self):
        self.sign_refresh = 0  # 刷新标志
        logger.info('代理IP刷新')
        self.DB.get_connect()
        self.init_data = self.DB.db_select("proxyIP")  # 初始数据库读取内容
        self.DB.db_close()
        self.__ip_synthesis()  # 代理IP表

    # IP与端口合成代理IP列表
    def __ip_synthesis(self):
        ip_list = []  # ip列表
        port_list = []  # 端口列表
        length = 0
        if self.init_data != None:
            for ip_port in self.init_data:
                ip_list.append(ip_port[0])
                port_list.append(ip_port[1])
                length += 1

        self.ip_list = ip_list
        self.port_list = port_list
        self.length = length

    # 随机获取一个代理IP
    # @return (ip, port)
    def get_proxy_ip(self):
        if self.sign_refresh > 100000:
            self.__ip_refresh()
        self.sign_refresh += 1
        choice_pos = choice(range(self.length))
        return self.ip_list[choice_pos], self.port_list[choice_pos]


if __name__ == '__main__':
    proxy_ip = ProxyIP()
    for i in range(10):
        print proxy_ip.get_proxy_ip()

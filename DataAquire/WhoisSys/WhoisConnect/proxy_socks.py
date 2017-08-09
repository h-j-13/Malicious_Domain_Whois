#!/usr/bin/env python
# encoding:utf-8

"""
    获取whois服务器的IP地址
=======================

version   :   1.0
author    :   @`13
time      :   2017.1.17

若希望使用代理socks获取whois,请自行购买或通过启发他方式取得,并将相关信息直接写入数据库
表 malicious_url_whois.whois_srvip 中
(包含了一部分样例参考)
"""

from random import choice

from __init__ import Info
from Setting.static import Static
from Database.db_opreation import DataBase
from Database.SQL_generate import SQL_generate

Static.init()
log_whois = Static.LOGGER


class ProxySocks(Info):
    """代理ip/socks类"""

    def __init__(self):
        self.proxy_socks_dict = {}
        self.__socks_refresh()

    def __socks_refresh(self):
        """代理刷新"""
        self.sign_refresh = 0  # 刷新标志
        log_whois.info('代理IP列表刷新')
        MySQL = DataBase()
        MySQL.db_connect()
        GET_PROXY_SQL = SQL_generate.PROXY_INFO(Static.PROXY_SOCKS_TABLE)
        self.init_data = MySQL.execute(GET_PROXY_SQL)  # 初始数据库读取内容
        MySQL.db_close()
        self.__socks_synthesis()  # 合成代理IP表

    def __socks_synthesis(self):
        """IP与端口合成代理列表"""
        log_whois.info('代理IP列表初始化')
        self.proxy_socks_dict = {}
        if self.init_data is not None:
            for result in self.init_data:
                whois_server_ip = result[0]
                one_proxy_ip = OneProxyIP(result[1], result[2], result[3],
                                          result[4], result[5])
                if self.proxy_socks_dict.get(whois_server_ip, None) is not None:
                    self.proxy_socks_dict[whois_server_ip].append(one_proxy_ip)
                else:
                    list_temp = []
                    list_temp.append(one_proxy_ip)
                    self.proxy_socks_dict.setdefault(whois_server_ip, list_temp)
        else:  # 获取不到域名 - 关闭socks代理功能
            Static.PROXY_SOCKS_FLAG = False

    def get_proxy_socks(self, whois_server):
        """根据whois 服务器地址/ip 随机获取一个代理IP
        @:return (ip, port, mode)"""
        self.sign_refresh += 1
        if self.sign_refresh > Static.PROXY_SOCKS_REFRESH:  # 定期刷新
            self.__socks_refresh()
        proxy_ip_list = self.proxy_socks_dict.get(whois_server, None)
        # log_whois.debug("proxy:"+str(proxy_ip_list))
        if proxy_ip_list is not None:
            return choice(proxy_ip_list)  # 返回随机一个代理ip
        else:
            return None


def OneProxyIP(ip, port, mode, message, speed):
    """一条代理socks信息的数据结构"""
    port = int(port)
    # 根据模式处理代理socks信息
    if mode == 'SOCKS4':
        proxy_socks_info = {'ip': ip,
                            'port': port,
                            'mode': mode,
                            'speed': speed}
    elif mode == 'SOCKS5':
        for i in range(len(message)):
            if message[i] == ';':
                break
        username = ''
        password = ''
        for a in range(i):
            username += message[a]
        for b in range(len(message) - i - 1):
            password += message[b + i + 1]
        proxy_socks_info = {'ip': ip,
                            'port': port,
                            'mode': mode,
                            'username': username,
                            'password': password,
                            'speed': speed}
    else:
        proxy_socks_info = {}
    return proxy_socks_info


if __name__ == '__main__':
    # Demo
    proxy_ip = ProxySocks()  # 初始化对象
    single = ProxySocks()
    print id(proxy_ip)
    print id(single)
    print proxy_ip.proxy_socks_dict  # 全部代理列表
    for i in range(10):  # 选择
        print proxy_ip.get_proxy_socks("whois.cnnic.cn")

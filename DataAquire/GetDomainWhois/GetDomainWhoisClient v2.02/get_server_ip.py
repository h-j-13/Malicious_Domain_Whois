# !/usr/bin/python
# encoding:utf-8

# 获取whois服务器的IP地址
# @author 王凯
# @version 1.0
# 2015.12.24

from random import choice
from db_operation import DataBase

class ServerIP():
    def __init__(self):
        db = DataBase()
        db.connect()
        self.whois_ip_dict = {}
        query_results = db.get_server_ip()
        for result in query_results:
            key = result.svr_name
            if not result.ip:
                continue
            ip_list = result.ip.split(',')
            values = []
            if result.port_available:
                port_available_list = list(result.port_available)
                for i, ip in enumerate(ip_list):
                    if port_available_list[i] == '1':
                        values.append(ip)
            self.whois_ip_dict.setdefault(key, values)
        db.close()

    # 获取whois服务器的ip地址
    # @param server_addr whois服务器
    # @return ip (若查找不到,返回None)
    def get_server_ip(self, server_addr):
        result = self.whois_ip_dict.get(server_addr, [])
        return None if not result else choice(result)

if __name__ == '__main__':
    print ServerIP().get_server_ip('whois.cnnic.cn')

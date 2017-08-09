# /usr/bin/python
# encoding:utf8

# 获取域名whois服务器地址
# @author 王凯
# @version 1.0
# 2015.12.23

from random import choice


class WhoisServerAddr:
    def __init__(self, db):
        server_addr_dict = {}
        results = db.query_all_whois_addr()
        for result in results:
            key = result.tld
            if not result.addr:
                continue
            values = result.addr.split(',')
            server_addr_dict.setdefault(key, values)
        self.server_addr_dict = server_addr_dict

    def get_server_addr(self, tld):
        if self.server_addr_dict.get('.' + tld, None) is None:
            return None
        else:
            return choice(self.server_addr_dict.get('.' + tld, None))


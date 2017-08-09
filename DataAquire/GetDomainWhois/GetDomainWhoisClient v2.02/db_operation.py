#!/usr/bin/python
# encoding:utf-8

# 数据库操作模块
# @author 王凯
#
# last-update: 2016.7.23
#              @`13
#              删除了暂时无用的代理ip部分，部分代码丢弃到ObsoleteFile

import peewee
import ConfigParser
cf = ConfigParser.ConfigParser()
cf.read("WhoisClient.conf")

db = peewee.MySQLDatabase(host=cf.get('DataBase', 'host'),
                          user=cf.get('DataBase', 'user'),
                          passwd=cf.get('DataBase', 'passwd'),
                          database='whois_relevant',
                          charset='utf8',
                          port=cf.getint('DataBase', 'port'))


class svr_ip(peewee.Model):
    svr_name = peewee.CharField()  # 服务器名称
    ip = peewee.CharField()  # 服务器IP表
    port_available = peewee.CharField()  # 可用数据表

    class Meta():
        database = db


class DataBase():
    def connect(self):
        db.connect()

    def close(self):
        db.close()

    # 获取server_ip 信息
    def get_server_ip(self):
        try:
            query_results = svr_ip.select(
                    svr_ip.svr_name, svr_ip.ip, svr_ip.port_available
                ).where(
                    svr_ip.port_available!=None
                )
            return query_results
        except peewee.OperationalError as e:
            raise e


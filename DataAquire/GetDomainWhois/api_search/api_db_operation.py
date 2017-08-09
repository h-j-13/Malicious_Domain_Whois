#!/usr/bin/python
# encoding:utf-8

# 数据库操作模块
# @author 王凯

import peewee

db = peewee.MySQLDatabase(host='172.26.253.3',
              user='root',
              passwd='platform',
              database='DomainWhois',
              charset='utf8',
              port=3306)


class proxy(peewee.Model):
    whois_server_ip = peewee.CharField()  # whois服务器IP
    ip = peewee.CharField()  # 代理IP
    port = peewee.IntegerField()  # 代理端口
    mode = peewee.IntegerField()  # 代理方式
    speed = peewee.DoubleField()  # 连接速度

    class Meta():
        database = db


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

    # 获取proxy_ip 信息
    def get_proxy_ip(self):
        try:
            query_results = proxy.select(
                    proxy.whois_server_ip, proxy.ip, proxy.port, proxy.mode, proxy.speed
            ).where(
                    proxy.speed != None, proxy.speed < 1
            )
            return query_results
        except peewee.OperationalError as e:
            raise e

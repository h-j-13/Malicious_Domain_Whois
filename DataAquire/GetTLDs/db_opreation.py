#!/usr/bin/python
# encoding:utf-8

#
# WhoisSrv获取-来自INNA
# func  : 数据库操作
# time  : old
# author: @`13
#

import MySQLdb
import threading
import time
import datetime
import ConfigParser


# 数据库操作类
class DataBase:
    """
    数据库操作类
    """
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read("GetTLDs.conf")
        self.host = cf.get('DataBase', 'host')
        self.user = cf.get('DataBase', 'user')
        self.passwd = cf.get('DataBase', 'passwd')
        self.charset = 'utf8'
        self.db_lock = threading.Lock()

    def get_connect(self):
        """链接数据库"""
        if self.db_lock.acquire():
            try:
                self.conn = MySQLdb.Connection(
                    host=self.host, user=self.user, passwd=self.passwd, charset=self.charset)
            except MySQLdb.Error, e:
                print str(datetime.datetime.now()).split(".")[0], "ERROR %d: %s" % (e.args[0], e.args[1])
            self.cursor = self.conn.cursor()
            if not self.cursor:
                raise(NameError, "Connect failure")
            self.db_lock.release()

    def db_close(self):
        """关闭数据库"""
        try:
            self.conn.close()
        except MySQLdb.Error as e:
            print 'db_close error_info: %d: %s' % (e.args[0], e.args[1])

    def db_commit(self):
        """提交事务"""
        try:
            self.conn.commit()
        except MySQLdb.Error as e:
            print 'db_commit error_info: %d: %s' % (e.args[0], e.args[1])

    def execute(self, sql):
        """执行SQL语句"""
        result = None
        if self.db_lock.acquire():
            try:
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
            except MySQLdb.Error, e:
                if e.args[0] == 2013 or e.args[0] == 2006: # 数据库连接出错，重连
                    self.db_lock.release()
                    self.get_connect()
                    print str(datetime.datetime.now()).split(".")[0], '数据库重新连接'
                    result = self.execute(sql) # 重新执行
                    self.db_lock.acquire()
                else:
                    print str(datetime.datetime.now()).split(".")[0], "ERROR %d: %s" % (e.args[0], e.args[1])
            self.db_lock.release()

        return result if result else None
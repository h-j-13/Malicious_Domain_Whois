# !/usr/bin/python
# encoding:utf-8

import MySQLdb
import threading
import time
import socket
from threading import Thread
from random import choice
from Queue import Queue
import datetime

#数据库操作类
class DataBase:
    '''
    数据库操作类
    '''
    def __init__(self):
        self.host = '172.29.152.249'
        self.user = 'root'
        self.passwd = 'platform'
        self.charset = 'utf8'
        self.db_lock = threading.Lock()

    #链接数据库
    def get_connect(self):
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

    #关闭数据库
    def db_close(self):
        try:
            self.conn.close()
        except MySQLdb.Error as e:
            print 'db_close error_info: %d: %s' % (e.args[0], e.args[1])

    #提交事务
    def db_commit(self):
        try:
            self.conn.commit()
        except MySQLdb.Error as e:
            print 'db_commit error_info: %d: %s' % (e.args[0], e.args[1])

    #执行SQL语句（取回所有结果）
    def execute(self, sql):
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


if __name__ == '__main__':
    DB =DataBase()
    DB.get_connect()
    for i in range(1,101):
        start = time.time()
        DB.execute("""select * from domain_whois.domain_whois_{num} where domain = 'baidu.com' """.format(num = i ))
        end = time.time()
        print end-start
    DB.db_close()
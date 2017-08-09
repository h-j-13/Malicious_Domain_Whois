#!/usr/bin/python
# encoding:utf-8

# 记录每个探测点的获取数量并存储到数据库
# @author `13


import MySQLdb
import threading
import time
import datetime
import ConfigParser
cf = ConfigParser.ConfigParser()
cf.read("WhoisClient.conf")
CLIENT_NUM = cf.get('client', 'number')
# 数据库操作类


class DataBase:
    """
    数据库操作类
    """
    def __init__(self):
        self.host = cf.get('DataBase', 'host')
        self.user = cf.get('DataBase', 'user')
        self.passwd = cf.get('DataBase', 'passwd')
        self.charset = 'utf8'
        self.db_lock = threading.Lock()

    # 链接数据库
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

    # 关闭数据库
    def db_close(self):
        try:
            self.conn.close()
        except MySQLdb.Error as e:
            print 'db_close error_info: %d: %s' % (e.args[0], e.args[1])

    # 提交事务
    def db_commit(self):
        try:
            self.conn.commit()
        except MySQLdb.Error as e:
            print 'db_commit error_info: %d: %s' % (e.args[0], e.args[1])

    # 执行SQL语句
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


#  计数类
class Count:
    def __init__(self):
        pass

    # 记录个数
    @staticmethod
    def updateCount(count):
        # #获取当前时间
        # current_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        DB = DataBase()
        DB.get_connect()
        # 获取数据库时间
        current_time = DB.execute("SELECT NOW();")[0][0]
        # print current_time

        # 更新记录
        DB = DataBase()
        DB.get_connect()
        SQL = """INSERT INTO whois_sys_log.client_count_log_{client_num} (time,count) VALUES('{current_time}','{count_num}');"""\
            .format(client_num=CLIENT_NUM, current_time=current_time, count_num=count)
        # print SQL
        DB.execute(SQL)
        DB.db_commit()
        DB.db_close()

    # 获取历史最大个数
    @staticmethod
    def getCount():
        DB = DataBase()
        DB.get_connect()

        SQL = """SELECT MAX(count) FROM whois_sys_log.client_count_log_{client_num};""".format(
            client_num=CLIENT_NUM )
        # print SQL
        max_count = DB.execute(SQL)[0][0]
        if not max_count:
            return 0
        # print max_count
        DB.db_close()
        return max_count


if __name__ == '__main__':

    DB = DataBase()
    DB.get_connect()
    print Count().getCount()
    DB.db_close()

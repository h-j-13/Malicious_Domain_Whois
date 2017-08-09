#!/usr/bin/env python
# encoding:utf-8

"""
    基于MySQL的数据库操作封装
=============================

version   :   1.0
author    :   @`13
time      :   2017.1.17
"""

import datetime
import MySQLdb
import threading

from Setting.static import Static

Static.init()
log_db = Static.LOGGER


class DataBase:
    """MySQL数据库操作类"""

    def __init__(self, ):
        """数据库配置初始化"""
        self.host = Static.HOST
        self.port = Static.PORT
        self.user = Static.USER
        self.passwd = Static.PASSWD
        self.charset = Static.CHARSET  # 以后统一使用数据库默认编码
        self.db_lock = threading.Lock()  # 数据库操作锁

    def db_connect(self):
        """连接数据库"""
        if self.db_lock.acquire():
            try:
                self.conn = MySQLdb.Connection(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    passwd=self.passwd,
                    charset=self.charset,
                    use_unicode=False)
            except MySQLdb.Error, e:
                log_db.error('connect error:' + str(e))
            self.cursor = self.conn.cursor()
            if not self.cursor:
                raise (NameError, "Connect failure")
            log_db.warning("数据库连接成功")
            self.db_lock.release()

    def db_close(self):
        """关闭数据库"""
        try:
            self.conn.close()
            log_db.warning('数据库关闭连接')
        except MySQLdb.Error as e:
            log_db.error('close error:' + str(e))

    def db_commit(self):
        """提交事务"""
        try:
            self.conn.commit()
            log_db.warning('提交事务')
        except MySQLdb.Error as e:
            log_db.error('commit error:' + str(e))

    def execute_no_return(self, sql):
        """
        执行SQL语句,不获取返回结果
        :param sql: SQL语句
        """
        log_db.info('执行:' + str(sql[:127]))
        if self.db_lock.acquire():
            try:
                self.cursor.execute(sql)
            except MySQLdb.Error, e:
                if e.args[0] == 2013 or e.args[0] == 2006:  # 数据库连接出错，重连
                    self.db_lock.release()
                    self.db_connect()
                    log_db.error('超时,数据库重新连接')
                    self.cursor.execute(sql)
                    self.db_lock.acquire()
                else:
                    log_db.error('execute_no_return error:' + str(e))
                    log_db.error('SQL : ' + sql)
                    self.db_lock.release()
                    return 'execute fail'
            self.db_lock.release()
        return 'execute success'

    def execute(self, sql):
        """
        执行SQL语句
        :param sql: SQL语句
        :return: 获取SQL执行并取回的结果
        """
        log_db.info('执行:' + str(sql[:127]))
        result = None
        if self.db_lock.acquire():
            try:
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
                self.db_lock.release()
            except MySQLdb.Error, e:
                if e.args[0] == 2013 or e.args[0] == 2006:  # 数据库连接出错，重连
                    self.db_lock.release()
                    self.db_connect()
                    log_db.error('超时,数据库重新连接')
                    result = self.execute(sql)  # 重新执行
                    self.db_lock.acquire()
                else:
                    self.db_lock.release()
                    log_db.error('execute error:' + str(e))
                    log_db.error('SQL : ' + sql)
        return result if result else None

    def execute_Iterator(self, sql, pretchNum=1000):
        """
        执行SQL语句(转化为迭代器)
        :param sql: SQL语句
        :param pretchNum: 每次迭代数目
        :return: 迭代器
        """
        log_db.info('执行:' + sql)
        Iterator_count = 0
        result = None
        result_list = []
        try:
                Resultnum = self.cursor.execute(sql)
                for i in range(Resultnum):
                    result = self.cursor.fetchone()
                    result_list.append(result)
                    Iterator_count += 1
                    if Iterator_count == pretchNum:
                        yield result_list
                        result_list = []
                        Iterator_count = 0
                yield result_list  # 最后一次返回数据
        except MySQLdb.Error, e:
                log_db.error('execute_Iterator error:' + str(e))
                log_db.error('SQL : ' + sql)


if __name__ == '__main__':
    # Demo
    DB = DataBase()
    DB.db_connect()
    SQL = """SELECT domain, whois_flag FROM {DB}.{domainTable} """.format(
        DB=Static.DATABASE_NAME, domainTable=Static.DOMAIN_TABLE)
    for result_list in DB.execute_Iterator(SQL):
        for result in result_list:
            print result
    DB.db_close()

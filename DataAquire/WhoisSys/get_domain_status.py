#!/usr/bin/env python
# encoding:utf-8

"""
    获取域名解析情况及状态
=======================

version   :   1.1
author    :   @`13
time      :   2017.04.09
time_v1.1 :   2017.04.24
"""

import Queue
import urllib2
import threading
import socket
from time import sleep

from Setting.static import Static  # 静态变量,设置
from Database.db_opreation import DataBase  # 数据库对象
from Database.SQL_generate import SQL_generate  # SQL语句生成器

Static.init()
global TaskQueue, ResultQueue
TaskQueue = Queue.Queue()  # 任务队列
ResultQueue = Queue.Queue()  # 结果队列


def work():
    """工作函数:获取域名的状态码以及解析情况,存入数据库"""
    global TaskQueue, ResultQueue
    while not TaskQueue.empty():
        domain = TaskQueue.get()
        available, HTTPcode = GetURLStatusCode(domain)
        r = [domain, available, HTTPcode]
        # Test - >
        print 'TEST->' + domain + ':',
        print r
        ResultQueue.put(r)
    return


def UpdateDate(DBObject, commitFrequency=Static.COMMIT_NUM):
    """工作函数:更新数据到数据库中"""
    global TaskQueue, ResultQueue
    count = 0
    while not (TaskQueue.empty() and ResultQueue.empty()):  # 当双队列不空时
        if not ResultQueue.empty():
            domain, available, HTTPcode = ResultQueue.get()
            # print domain, available, HTTPcode
            SQL = SQL_generate.UPDATE_DOMAIN_HTTP_STATUS(
                Static.HTTP_DOMAIN_TABLE,
                domain,
                available,
                HTTPcode)
            DBObject.execute_no_return(SQL)
            count += 1
            if count >= commitFrequency:
                DBObject.db_commit()
                count = 0
        else:
            sleep(0.5)
    return


def GetURLStatusCode(URL):
    """
    核心函数:获取域名的访问情况以及状态码
    :param URL: url / domain (域名会转换为标准url)
    :return: 此url的解析情况 1-可访问 9-不可访问
                    以及状态码
    """
    # 设置初始化
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    base_url = "http://www."
    if URL.find('http') == -1:
        URL = base_url + URL
    # print URL
    # 发送请求
    req = urllib2.Request(url=URL, headers=headers)
    try:
        return 1, urllib2.urlopen(req, timeout=Static.HTTP_TIME_OUT).code
    except urllib2.HTTPError, e:
        return 9, e.code
    except urllib2.URLError, e:
        # print e.reason
        return 9, -1
    except socket.error, e:
        if e.errno == 104:  # 被服务器拒绝错误 flag -> 8 [errno 104]:connetction reset by peer
            return 8, -1
        return 9, -1
    except:
        return 7, -1  # 其他所有异常 (例如 BadStatusLine flag -> 7


def GetDomain(DBObject, work_type):
    """
    获取需要判断解析情况的域名的域名
    :param DBObject: 数据库操作对象
    :param work_type: 工作类型,同主函数
    :return: 将所需数据存入 taskQueue
    """
    global TaskQueue
    sql = SQL_generate.GET_DOMAIN_FOR_HTTP_STATUS(Static.DOMAIN_TABLE, work_type)
    for resultpart in DBObject.execute_Iterator(sql):
        for result in resultpart:
            TaskQueue.put(str(result[0]))


def main(work_type=0):
    """
    主流程
    :param work_type: 工作类型  0：获取全部域名数据
                               1：获取新数据
                              -1: 重新探测失败数据
    """
    # 初始化
    global TaskQueue, ResultQueue
    DB = DataBase()
    DB.db_connect()
    init_sql = """USE {DB}""".format(DB=Static.HTTP_DATEBASE)
    DB.execute_no_return(init_sql)

    # 获取任务域名
    GetDomain(DB, work_type)

    # 开始获取域名解析情况
    thread_list = []
    for i in range(Static.HTTP_PROCESS_NUM):
        get_whois_thread = threading.Thread(target=work)
        get_whois_thread.setDaemon(True)
        get_whois_thread.start()
        thread_list.append(get_whois_thread)

    # 开始域名字典,更新数据库
    sleep(Static.HTTP_TIME_OUT)  # 等待队列填充
    update_whois_thread = threading.Thread(target=UpdateDate(DB))
    update_whois_thread.setDaemon(True)
    update_whois_thread.start()
    thread_list.append(update_whois_thread)

    # 挂起进程直到结束
    for update_whois_thread in thread_list:
        update_whois_thread.join()
    print "域名解析情况获取结束"

    # 清空队列
    while not TaskQueue.empty():
        TaskQueue.get()
    while not ResultQueue.empty():
        ResultQueue.get()
    DB.db_commit()
    DB.db_close()


if __name__ == '__main__':
    main(0)
    for i in range(3):
        main(-1)

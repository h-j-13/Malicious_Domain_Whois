#!/usr/bin/env python
# encoding:utf-8

"""
    主流程-程序入口
=====================

version   :   1.0
author    :   @`13
time      :   2017.2.11
"""


import Queue
import threading
from time import sleep

from Database.db_opreation import DataBase  # 数据库对象
from Database.update_record import WhoisRecord  # 更新信息函数
from get_domain_whois import get_domain_whois  # 获取whois函数
from Setting.static import Static  # 静态变量,设置

Static.init()
log_main = Static.LOGGER

global DomainQueue, WhoisQueue
DomainQueue = Queue.Queue()  # 任务域名队列
WhoisQueue = Queue.Queue()  # whois结果队列

global Process_Num, Ban_Setting
Process_Num = Static.PROCESS_NUM  # 获取进程数
Ban_Setting = False  # 防Ban设置


def GetWhois():
    """获取whois,并放入Whois队列中"""
    global DomainQueue, WhoisQueue
    while not DomainQueue.empty():
        domain, flag = DomainQueue.get()
        result = get_domain_whois(domain)
        print result
        if result:
            WhoisQueue.put([result, flag])
        if Ban_Setting:
            sleep(0.1)  # 防ban
    return


def WriteWhoisInfo(DataBaseObject):
    """更新whois数据到数据库中"""
    global DomainQueue, WhoisQueue
    WhoisInfoDict = WhoisRecord(DataBaseObject)
    while not (WhoisQueue.empty() and DomainQueue.empty()):  # 当双队列不空时候:
        if not WhoisQueue.empty():
            whois_dict, old_flag = WhoisQueue.get()
            WhoisInfoDict.Update(whois_dict, old_flag)
        else:
            sleep(0.5)


def main(Worktype=0):
    """
    主流程函数,获取whois并更新到数据库中
    :param Worktype: 工作方式  0 - 获取新增域名
                              1 - 重新获取所有域名数据
                             -1 - 获取失败域名
                            SQL - 特定获取域名的SQL语句
    """
    # 全局变量声明
    global Process_Num, Ban_Setting
    global DomainQueue, WhoisQueue
    # 初始化操作对象
    DB = DataBase()
    DB.db_connect()
    # 填充域名队列
    SQL = """SELECT domain, whois_flag FROM {DB}.{domainTable} """.format(
        DB=Static.DATABASE_NAME, domainTable=Static.DOMAIN_TABLE)
    if Worktype == 0:
        SQL += """WHERE whois_flag = -99 """
        log_main.error("新增域名whois获取任务开始...")
    elif Worktype == 1:
        pass
    elif Worktype == -1:
        Process_Num = Static.PROCESS_NUM_LOW  # 修改进程数
        Ban_Setting = True  # 开启防ban设置
        SQL += """WHERE whois_flag < 0 """
        log_main.error("定时探测任务开始...")
    elif type(Worktype) == str:
        SQL = Worktype
        Process_Num = Static.PROCESS_NUM_LOW  # 修改进程数
        Ban_Setting = True  # 开启防ban设置
        log_main.error("特定探测任务开始... + " + Worktype)
    else:
        log_main.error("unexcept arg - main function")
        return
    domian_list = DB.execute(SQL)
    if domian_list is None:
        log_main.error("未获取到域名..")
        return
    for result_list in DB.execute_Iterator(SQL):    # 使用<迭代器>减缓数据库IO
        for result in result_list:
            domain = result[0]
            flag = result[1]
            DomainQueue.put([str(domain).strip(), flag])
    log_main.error("域名获取完成 共 " + str(DomainQueue.qsize()) + " 个域名")
    # 开始多线程获取域名
    thread_list = []
    for i in range(Process_Num):
        get_whois_thread = threading.Thread(target=GetWhois)
        get_whois_thread.setDaemon(True)
        get_whois_thread.start()
        thread_list.append(get_whois_thread)
    # 开始域名字典,更新数据库
    sleep(Static.SOCKS_TIMEOUT)  # 等待队列填充
    update_whois_thread = threading.Thread(target=WriteWhoisInfo(DB))
    update_whois_thread.setDaemon(True)
    update_whois_thread.start()
    thread_list.append(update_whois_thread)
    # 挂起进程直到结束
    for update_whois_thread in thread_list:
        update_whois_thread.join()
    log_main.error("结束")
    # 清空队列
    while not WhoisQueue.empty():
        WhoisQueue.get()
    while not DomainQueue.empty():
        DomainQueue.get()
    DB.db_commit()
    DB.db_close()


if __name__ == '__main__':
    print "whois探测开始"
    main(0)
    main(0)
    main(1)
    main(-1)

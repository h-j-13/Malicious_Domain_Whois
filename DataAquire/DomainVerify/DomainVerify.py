# !/usr/bin/python
# encoding:utf-8

# time：2016.7.11
# func：验证域名是否存在
#         提供两种方式：
#             1,更新在数据库中的字段，
#             2,把结果写成txt文件.
#         version 1.3:
#               改位使用线程池。
# author：@`13

import MySQLdb
import threading
import time
import socket
from threading import Thread
from random import choice
from Queue import Queue
import datetime

#Whois服务器地址列表
com_host_list = '199.7.58.74,199.7.51.74,199.7.60.74,199.7.55.74,199.7.50.74,199.7.74.74,199.7.54.74,199.7.48.74,199.7.56.74,199.7.71.74,199.7.49.74,199.7.53.74,199.7.59.74,199.7.57.74,199.7.61.74,199.7.73.74,199.7.52.74'.split(',')
cn_host_list = '218.241.97.14'.split(',')
hk_host_list = '203.119.87.74,203.119.2.74'.split(',')
net_host_list = '199.7.58.74,199.7.51.74,199.7.60.74,199.7.55.74,199.7.50.74,199.7.74.74,199.7.54.74,199.7.48.74,199.7.56.74,199.7.71.74,199.7.49.74,199.7.53.74,199.7.59.74,199.7.57.74,199.7.61.74,199.7.73.74,199.7.52.74'.split(',')
org_host_list = '199.15.84.131'.split(',')
edu_host_list = '216.85.144.196'.split(',')
gov_host_list = '199.7.51.77,199.7.74.77,199.7.50.77,199.7.48.77,199.7.59.77,199.7.53.77,199.7.52.77,199.7.54.77'.split(',')
info_host_list = '199.15.85.130'.split(',')
biz_host_list = '209.173.57.169,209.173.53.169'.split(',')
wang_host_list = '1.8.102.129,202.173.11.141'.split(',')
top_host_list = '1.8.102.129,202.173.11.141'.split(',')

#重写超时方法
class TimeoutException(Exception):
    pass

ThreadStop = Thread._Thread__stop # 获取私有函数

#超时设置
def timelimited(timeout):
    def decorator(function):
        def decorator2(*args, **kwargs):
            class TimeLimited(Thread):
                def __init__(self, _error=None,):
                    Thread.__init__(self)
                    self._error = _error

                def run(self):
                    try:
                        self.result = function(*args, **kwargs)
                    except Exception, e:
                        self._error = e

                def _stop(self):
                    if self.isAlive():
                        ThreadStop(self)

            t = TimeLimited()
            t.setDaemon(True) # 守护线程
            t.start()
            t.join(timeout)

            if isinstance(t._error, TimeoutException):
                t._stop()
                raise TimeoutException('timeout for %s' % (repr(function)))

            if t.isAlive():
                t._stop()
                raise TimeoutException('timeout for %s' % (repr(function)))

            if t._error is None:
                return t.result

        return decorator2
    return decorator

#验证域名是否存在
def verification(domain):
    '''
    :param domain:域名
    :return: 域名存在状态(False-不存在/True-存在)
    '''
    result = ''
    for i in range(2):
        tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = get_recv_info(tcpCliSock, domain)
            tcpCliSock.close()
        except Exception:
            result = ''
        if result != '':
            break

    #print result
    #time.sleep(10)

# 不存在关键词

# No matching
# not been registered
# No Match
# No match for
# NOT FOUND
# Not found
# not exist

    #print  result
    if result != None:
        if result.find('No match') != -1 or \
            result.find('No matching') != -1 or \
            result.find('not been registered') != -1 or \
            result.find('No match for') != -1 or \
            result.find('NOT FOUND') != -1 or \
            result.find('Not found') != -1 or \
             result.find('not exist') != -1:
            return False
        else:
            return True
    else:
        return False

#设置超时时间
@timelimited(10)

#与whois服务器通信取得信息
def get_recv_info(tcpCliSock, domain):
    if domain.split('.', 1)[1] == 'com':
        HOST = choice(com_host_list)
    elif domain.split('.', 1)[1] == 'cn':
        HOST = choice(cn_host_list)
        #print HOST
    elif domain.split('.', 1)[1] == 'hk':
        HOST = choice(hk_host_list)
    elif domain.split('.', 1)[1] == 'net':
        HOST = choice(net_host_list)
    elif domain.split('.', 1)[1] == 'org':
        HOST = choice(org_host_list)
    elif domain.split('.', 1)[1] == 'edu':
        HOST = choice(edu_host_list)
    elif domain.split('.', 1)[1] == 'gov':
        HOST = choice(gov_host_list)
    elif domain.split('.', 1)[1] == 'info':
        HOST = choice(info_host_list)
    elif domain.split('.', 1)[1] == 'biz':
        HOST = choice(biz_host_list)
    elif domain.split('.', 1)[1] == 'wang':
        HOST = choice(wang_host_list)
    elif domain.split('.', 1)[1] == 'top':
        HOST = choice(top_host_list)

    data_result = ""
    PORT = 43           # 端口
    BUFSIZ = 1024       # 每次返回数据大小
    ADDR = (HOST, PORT) # 地址
    EOF = "\r\n"        # EOF
    data_send = domain + EOF

    #尝试通信
    try:
        tcpCliSock.connect(ADDR)
        tcpCliSock.send(data_send)
    except socket.error, e:
        return

    while True:
        try:
            data_rcv = tcpCliSock.recv(BUFSIZ)
        except socket.error, e:
            return
        if not len(data_rcv):
            return data_result                  # 返回查询结果
        data_result = data_result + data_rcv    # 每次返回结果组合


#数据库操作类
class DataBase:
    '''
    数据库操作类
    '''
    def __init__(self):
        self.host = '172.26.253.3'
        self.user = 'root'
        self.passwd = 'platform'
        self.charset = 'utf8'
        self.domain_queue = Queue(-1)
        self.file = open('result_0.txt', 'w') # 默认写入文件（一般没用）
        self.file_count = 1
        self.count = 0                      # commit计数
        self.count_lock = threading.Lock()  # count锁
        self.queue_lock = threading.Lock()
        self.db_lock = threading.Lock()

    #切换记录结果文件
    def change_write_file(self, tld):
        self.file.close()
        file_name = 'result_' + tld + str(self.file_count) + '.txt'
        print '完成了', str(self.file_count), '个文件'
        self.file_count += 1
        self.file = open(file_name, 'w')

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

    #执行SQL语句 并取回相应的域名，转化成生成器
    def execute_fetch(self, sql, fetch_num=5000):
        result_list = []
        temp_domain = ''
        count = 0

        if self.db_lock.acquire():
            try:
                total_num = self.cursor.execute(sql)
                for i in range((total_num//fetch_num) + 1):
                    if total_num - count > fetch_num:
                        num = fetch_num
                    else:
                        num = total_num % fetch_num
                    for j in range(num):
                        temp_domain = self.cursor.fetchone() #[0] 视SQL语句而定 是否是 SELETE *
                        #print temp_domain
                        result_list.append(temp_domain)

                    count += len(result_list)
                    yield result_list
                    result_list = []

            except MySQLdb.Error, e:
                if e.args[0] == 2013 or e.args[0] == 2006:  # 数据库连接出错，重连
                    self.db_lock.release()
                    self.get_connect()
                    print str(datetime.datetime.now()).split(".")[0], '数据库重新连接'
                    self.execute_fetch(sql,)                # 递归，重新执行
                                                                # 这里重连之后会全部执行之前命令，就是会获得重复的结果，暂时未修改
                    self.db_lock.acquire()
                else:
                    print str(datetime.datetime.now()).split(".")[0], "ERROR %d: %s" % (e.args[0], e.args[1])
            self.db_lock.release()

    #  ================================================
    # #工作函数：(数据库）
    # def func(self, table, tld):
    #     self.table = table
    #     self.tld = tld
    #     self.get_connect()
    #     try:
    #         #获取域名的SQL语句
    #         sql = """SELECT domain FROM {table_name} WHERE {tld} IS NULL """\
    #                 .format(table_name = self.table,tld = self.tld)
    #         domain_list = self.execute(sql)
    #                                 # 有几个不是ANSI的域名 容易报错
    #         while len(domain_list) >= 10:
    #             for domain in domain_list:
    #                 #讲域名放入队列
    #                 self.domain_queue.put(domain[0]+'.'+self.tld)
    #
    #             thread_list = []
    #             for i in range(30):
    #                 thread_temp = threading.Thread(target=self.verification_thread)
    #                 thread_temp.start()
    #                 thread_list.append(thread_temp)
    #
    #             for thread_temp in thread_list:
    #                 thread_temp.join()
    #
    #             self.db_commit()
    #             domain_list = self.execute(sql)
    #
    #     except MySQLdb.Error as e:
    #         print e
    # ================================================

    #工作函数：（文件）
    def func(self, table, tld, lines=500000):
        self.count = 0                          #换TLD后重置位0
        self.lines = lines
        self.table = table
        self.tld = tld
        self.get_connect()
        self.change_write_file(tld)
        try:
            #获取域名的SQL语句
            sql = """SELECT domain FROM {table_name} WHERE {tld} IS NULL """\
                    .format(table_name=self.table, tld=self.tld)
                                    # PS：有几个不是ANSI的域名 容易报错

            # 使用迭代器，减小内存占用
            for domain_list in self.execute_fetch(sql):
                for domain in domain_list:
                    #讲域名放入队列
                    self.domain_queue.put(domain[0]+'.'+self.tld)

                thread_list = []
                for i in range(30):
                    thread_temp = threading.Thread(target=self.verification_thread)
                    thread_temp.start()
                    thread_list.append(thread_temp)

                for thread_temp in thread_list:
                    thread_temp.join()
		
                # self.db_commit()
		
            self.file.close()

        except MySQLdb.Error as e:
            print e

    # 验证线程
    def verification_thread(self):
        #注意队列的锁
        while True:
            if self.queue_lock.acquire():
                if self.domain_queue.qsize() == 0:
                    self.queue_lock.release()
                    break
                else:
                    domain = self.domain_queue.get()
                    self.queue_lock.release()
                flag = 1 if verification(domain) else 0

                #数据库操作部分
		#====================================================
                #print domain + '\tflag:\t' + str(flag)
                # DOMAIN = domain.split('.',1)[0]
                # TLD = domain.split('.',1)[1]
                # sql = """UPDATE {table} SET {tld} = {flag} WHERE domain = '{domain}';""".format(
                #     table=self.table, tld=TLD, domain=DOMAIN, flag=flag)
                # self.execute(sql)
		#======================================================
                if self.count_lock.acquire():

                    tmp = domain + '\t' + str(flag)
                    # print tmp
                    try:
                        self.file.write(str(tmp))
                    except UnicodeEncodeError, e:
                        if str(e).find('ascii') != -1:
                            pass
                        else:
                            print e
                    self.file.write('\n') #换行
                    self.count += 1

                    if self.count >= self.lines:
                        self.change_write_file(self.tld)
                        self.count = 0
                    self.count_lock.release()


if __name__ == '__main__':

    DB = DataBase()
    DB.get_connect()


    #参数说明。func（获取域名的表名，探测的tld名字，一个文件的行数（缺省值为 500 000）
    #DB.func('HJ.domains_all', 'com', lines=500000)
    # # # # # # # # # # # # # # # # # # # # # # # #
    #DB.func('HJ.domains_3', 'com', lines=500000)
    #DB.func('HJ.domains_3', 'cn', lines=500000)
    #DB.func('HJ.domains_3', 'hk', lines=500000)
    #DB.func('HJ.domains_3', 'net', lines=500000)
    #DB.func('HJ.domains_3', 'org', lines=500000)
    #DB.func('HJ.domains_3', 'edu', lines=500000)
    DB.func('HJ.domains_3', 'gov', lines=500000)
    DB.func('HJ.domains_3', 'info', lines=500000)
    DB.func('HJ.domains_3', 'com', lines=500000)
    DB.func('HJ.domains_3', 'biz', lines=500000)
    DB.func('HJ.domains_3', 'wang', lines=500000)
    DB.func('HJ.domains_3', 'top', lines=500000)
    # # # # # # # # # # # # # # # # # # # # # # # #
    DB.func('HJ.domains_last_3', 'com', lines=500000)
    DB.func('HJ.domains_last_3', 'cn', lines=500000)
    DB.func('HJ.domains_last_3', 'hk', lines=500000)
    DB.func('HJ.domains_last_3', 'net', lines=500000)
    DB.func('HJ.domains_last_3', 'org', lines=500000)
    DB.func('HJ.domains_last_3', 'edu', lines=500000)
    DB.func('HJ.domains_last_3', 'gov', lines=500000)
    DB.func('HJ.domains_last_3', 'info', lines=500000)
    DB.func('HJ.domains_last_3', 'com', lines=500000)
    DB.func('HJ.domains_last_3', 'biz', lines=500000)
    DB.func('HJ.domains_last_3', 'wang', lines=500000)
    DB.func('HJ.domains_last_3', 'top', lines=500000)

    DB.db_close()

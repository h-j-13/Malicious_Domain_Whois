# usr/bin/python
# encoding:utf-8

# whois 信息获取，客户端
# @author 王凯
# version 2.02

# -history_version-
# version 2.01：增加统计功能
#
# last-update ：2016.7.22
# last-version：2.02
# change_func ： 增加读取配置文件的功能，
#               重构部分代码，
#               删除了目前没有用到的代理ip，
#               部分代码丢弃到ObsoleteFile;
# author      ：@`13

import time
import json
import pika
import re
# from gevent import monkey
# monkey.patch_socket()
# import gevent
from whois_connect import GetWhoisInfo
from whois_connect import WhoisConnectException
import datetime
import threading
import ConfigParser
import count_log

# 统计，日志功能
C = count_log.Count()
count = C.getCount()
count_lock = threading.Lock()

# 配置文件
cf = ConfigParser.ConfigParser()
cf.read("WhoisClient.conf")

TIMEOUT = cf.getint('socket', 'timeout')
RECONNECT = cf.getint('socket', 'reconnect')

channel_whois = None
RABBITMQ_HOST = cf.get('RabbitMQ', 'host')  # rabbitmq_host
THREAD_NUM = cf.getint('RabbitMQ', 'thread')
INTERVAL_TIME = cf.getint('RabbitMQ', 'interval')

RECORD_INTERVAL = cf.getint('client', 'interval')
MONITOR_FLAG = cf.getint('client', 'monitor_flag')

if MONITOR_FLAG:
    WhoisDetail_log = open('whois_detail_log.txt', 'a')
    WhoisDetail_log.write("Whois返回信息记录：")
    log_lock = threading.Lock()


# 初始化通信队列
def init_queue():
    global channel_whois
    connect = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel_whois = connect.channel()
    channel_whois.queue_declare(queue='whois_queue', durable=True)


# 客户端数据提取线程
def thread_client():
    connect = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel_domain = connect.channel()
    channel_domain.basic_qos(prefetch_count=1)
    channel_domain.basic_consume(domain_pull,
                                 queue='domain_queue',
                                 no_ack=False, )
    channel_domain.start_consuming()


# 提取域名队列中的信息
def domain_pull(ch, method, properties, body):
    domain_info = json.loads(body)
    global count, count_lock
    if count_lock.acquire():
        count += 1
        if count % RECORD_INTERVAL == 0:
            print str(datetime.datetime.now()).split('.')[1], '完成:', count
            C.updateCount(count)
        count_lock.release()
    whois_server_first = domain_info['whois_srv']
    func_name = domain_info['func_name']
    domain = domain_info['domain']
    exist = domain_info['exist']

    print domain

    flag_error = '0'  # 错误标志
    flag_first_error = '000'  # 一级错误
    flag_sec_error = '000'  # 二级错误
    whois_server_sec = ''  # 二级服务器
    whois_details = ''  # 返回数据

    # 可能存在二级服务器
    if func_name == 'com_manage':
        whois_details_first = ''
        try:
            whois_details_first = GetWhoisInfo(domain, whois_server_first).get()
            if xxx_bool(whois_details_first):
                whois_details_first = GetWhoisInfo('=' + domain, whois_server_first).get()
        except WhoisConnectException as e:
            flag_error = '1'
            flag_first_error = bin(int(str(e)))[2:]
            flag_first_error = '0' * (3 - len(flag_first_error)) + flag_first_error

        whois_details_sec = None
        try:
            whois_server_sec = get_sec_server(whois_details_first, domain)
            if whois_server_sec:
                whois_details_sec = GetWhoisInfo(domain, whois_server_sec).get()
        except WhoisConnectException as e:
            flag_error = '1'
            flag_sec_error = bin(int(str(e)))[2:]
            flag_sec_error = '0' * (3 - len(flag_sec_error)) + flag_sec_error
            whois_details = whois_details_first
        else:
            whois_details = whois_details_sec
    else:
        try:
            whois_details = GetWhoisInfo(domain, whois_server_first).get()
        except WhoisConnectException as e:
            flag_error = '1'
            flag_first_error = bin(int(str(e)))[2:]
            flag_first_error = '0' * (3 - len(flag_first_error)) + flag_first_error
            flag_sec_error = '000'

    # 测试日志功能
    if MONITOR_FLAG:
        global WhoisDetail_log, log_lock

        if log_lock.acquire():
            WhoisDetail_log.write(whois_details)
            WhoisDetail_log.write('\n')
        log_lock.release()

    print whois_details,"---falg",flag_first_error
    whois_push(
        domain=domain,
        top_whois_server=whois_server_first,
        sec_whois_server=whois_server_sec,
        whois_details=whois_details,
        result_flag='1' + flag_error + flag_first_error + flag_sec_error,  # 结果标志
        func_name=func_name,
        exist=exist
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 返回处理完成确认信息


def whois_push(**whois_recv_info):
    global channel_whois
    # print 'whois push:', whois_recv_info
    result = ''
    try:
        result = json.dumps(whois_recv_info)
    except UnicodeDecodeError:
        for key in whois_recv_info.keys():
            if type(whois_recv_info[key]) == str:
                whois_recv_info[key] = whois_recv_info[key].decode('latin-1').encode("utf-8")
        result = json.dumps(whois_recv_info)
    if result != '':
        channel_whois.basic_publish(
            exchange='',
            routing_key='whois_queue',
            body=json.dumps(result),
            properties=pika.BasicProperties(
                delivery_mode=2)
        )


# 用来判断com_manage函数中，得到的whois信息是否包含xxx标志，若包括则需要重新发送
def xxx_bool(data):
    if data.find('\"xxx\"') != -1 and data.find('\"=xxx\"') != -1:
        return True
    else:
        return False


# 提取com_manage中whois信息中的，二级whois服务器名称
def get_sec_server(data, domain):
    if not data:
        return False
    if data.find("Domain Name: %s" % domain.upper()) != -1:
        pos = data.find("Domain Name: %s" % domain.upper())
        data = data[pos:]
        pattern = re.compile(r"Whois Server:.*|WHOIS Server:.*")
        sec_whois_server = ''
        for match in pattern.findall(data):
            if match.find('Server:') != -1:
                sec_whois_server = match.split(':')[1].strip()
        return False if sec_whois_server == '' else sec_whois_server
    elif data.find('Registrar WHOIS Server:') != -1:  # ws二级服务器
        pattern = re.compile(r'Registrar WHOIS Server:.*?')
        sec_whois_server = ''
        for match in pattern.findall(data):
            if match.find('Server:') != -1:
                sec_whois_server = match.split(':')[1].strip()
        return False if sec_whois_server == '' else sec_whois_server
    else:
        return False


# 开启20个客户端线程
def main():
    print "Whois 客户端正在初始化..."
    init_queue()  # 初始化通信队列
    print "Whois 客户端正在运行..."
    import threading

    # 获取不到内容就挂起，按时检测一次
    #   大部分时间在线程中空转
    #   线程 -> 获取域名 -> 开始尝试解析 -> 获取数据 -> 填入whois队列/返回domain回执信息 -> ...
    thread_list = []
    for i in range(THREAD_NUM):
        client_thread = threading.Thread(target=thread_client)
        client_thread.setDaemon(True)
        client_thread.start()
        thread_list.append(client_thread)
    for client_thread in thread_list:
        client_thread.join()

if __name__ == '__main__':
    main()
    main()
    main()

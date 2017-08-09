# /usr/bin/python
# encoding:utf-8

# 程序入口
# @version 2.01
# @author 王凯

# -history_version-
#
# last-update ：2016.7.22
# last-version： 2.01
# change_func ： 增加读取配置文件的功能，
#                重构部分代码，
#                更换了提取域名逻辑。
# author      ：@`13

import json
import pika
import threading
import time

from Queue import Queue
from static import Static

Static.init()
from domain_analyse import DomainAnalyse
from update_record import update_record, update_not_deal_method, update_not_tld_record
from api_search import api_main
import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read("test.conf")

WAIT_INTERVAL = cf.getint("test", "wait_interval")
MONITOR_INTERVAL = cf.getint("test", "monitor_interval")
QUEUE_LENGTH_MAX = cf.getint("test", "queue_length_max_limit")
QUEUE_LENGTH_MIN = cf.getint("test", "queue_length_min_limit")
DOMAIN_SOURCE_TABLE_NUM = cf.getint("test", "domain_source_num")


# 任务分发类，向工作队列中添加域名
class WorkDispatch:
    def __init__(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            Static.RABBITMQ_HOST))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='domain_queue', durable=True)  # 域名队列

    # 开启任务分发
    def open_dispatch(self):
        dispatch_thread = threading.Thread(target=self.dispatch_thread)
        dispatch_thread.setDaemon(True)
        dispatch_thread.start()

    # 任务分发线程
    def dispatch_thread(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            Static.RABBITMQ_HOST))
        channel = connection.channel()
        # 域名数据添加
        domain_queue = self.get_domain()
        while domain_queue.qsize() > 0:
            while domain_queue.qsize() > 0:
                now_count = channel.queue_declare(queue='domain_queue', durable=True).method.message_count
                #  队列中域名过少
                if now_count < QUEUE_LENGTH_MIN:
                    #  向队列中添加域名，直到域名数量超过最大值
                    while now_count < QUEUE_LENGTH_MAX:
                        if domain_queue.qsize() >= 100:
                            self.domain_push(domain_queue.get(), True)
                        else:
                            domain_queue = self.get_domain()
                        now_count = channel.queue_declare(queue='domain_queue', durable=True).method.message_count
                    #  超过最大值后，挂起一段时间
                    time.sleep(WAIT_INTERVAL)

                # 隔一段时间后检测队列，过少时重新开始添加。
                time.sleep(MONITOR_INTERVAL)
                if domain_queue.qsize() < 100:
                    domain_queue = self.get_domain()

    def get_domain(self):
        domain_queue = Queue(-1)
        i = 1
        while i <= DOMAIN_SOURCE_TABLE_NUM:
            for domain in Static.whois_db.get_not_deal_domains(i, Static.FINISHED_TLD):
                domain_queue.put(domain)
            i += 1
        print Static.get_now_time(), '提取出域名: ', domain_queue.qsize()
        return domain_queue

    # 任务域名添加
    # @param domain 域名
    # @param exist 数据库是否存在
    def domain_push(self, domain, exist):
        do_an = DomainAnalyse(domain)
        domain_punycode = do_an.get_punycode_domain()  # punycode编码域名
        tld = do_an.get_punycode_tld()  # 域名后缀
        whois_srv = Static.whois_addr.get_server_addr(tld)

        if tld == 'za':
            if domain.find('co.za') != -1:
                whois_srv = 'whois.registry.net.za'
            elif domain.find('web.za') != -1:
                whois_srv = 'web-whois.registry.net.za'
            elif domain.find('org.za') != -1:
                whois_srv = 'org-whois.registry.net.za'
            elif domain.find('net.za') != -1:
                whois_srv = 'net-whois.registry.net.za'

        # 无该域名后缀记录
        if whois_srv is None:
            update_not_tld_record(domain, exist)
            return
        func_name = Static.func_name.get_func_name(whois_srv)
        if func_name is None:
            update_not_deal_method(domain, exist)
            return
        else:
            domain_info = {'domain': domain_punycode,
                           'whois_srv': whois_srv,
                           'func_name': func_name,
                           'exist': exist
                           }
            # print 'domain push:', domain_info['domain']
            self.channel.basic_publish(
                exchange='',
                routing_key='domain_queue',
                body=json.dumps(domain_info),
                properties=pika.BasicProperties(
                    delivery_mode=2, )
            )


# whois信息队列监控类
class WhoisQueueMonitor:
    # 初始化声明队列
    def __init__(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            Static.RABBITMQ_HOST))
        channel_whois = connection.channel()
        channel_whois.queue_declare(queue='whois_queue', durable=True)  # whois队列
        self.count = 0  # commit 计数
        self.count_lock = threading.Lock()  # count 计数锁

    # 打开监控
    def open_monitor(self):
        monitor_thread_list = []
        # 开启多线程whois处理程序
        for i in range(Static.PROCESS_MAX):
            whois_monitor_thread = threading.Thread(target=self.monitor_thread)
            whois_monitor_thread.setDaemon(True)
            whois_monitor_thread.start()
            monitor_thread_list.append(whois_monitor_thread)

        for monitor_thread in monitor_thread_list:
            monitor_thread.join()

    # 监控线程
    def monitor_thread(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            Static.RABBITMQ_HOST))
        channel_whois = connection.channel()
        channel_whois.queue_declare(queue='whois_queue', durable=True)
        channel_whois.basic_qos(prefetch_count=1)
        channel_whois.basic_consume(
            self.whois_pull,
            queue='whois_queue',
            no_ack=False)
        channel_whois.start_consuming()

    # whois接收信息结果提取
    def whois_pull(self, ch, method, properties, body):
        recv_info_from_client = json.loads(body)
        if type(recv_info_from_client) == unicode:
            recv_info_from_client = json.loads(recv_info_from_client)
        # print 'whois pull:', recv_info_from_client['domain']
        update_record(recv_info_from_client)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # 返回处理完成确认信息
        if self.count_lock.acquire():
            self.count += 1
            if self.count > Static.COMMIT_NUM:
                Static.whois_db.db_commit()  # commit 操作
                print 'Commit: ', Static.get_now_time()
                self.count = 0
            self.count_lock.release()


# 程序主入口
def main():
    print Static.get_now_time(), ' Start'
    # api_main.open_search_api()  # 打开api服务器
    Static.whois_db.connect()  # 数据库连接
    WorkDispatch().open_dispatch()  # 开启任务分发
    WhoisQueueMonitor().open_monitor()  # 开启whois队列监控


if __name__ == '__main__':
    main()

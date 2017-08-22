#coding:utf-8
import os
import Queue
import threading
import exceptions
import HtmlDownloader
import ProxyHelper
import config
from time import sleep

proxy_object=ProxyHelper.ProxyHelper()

#负责维护代理池
def proxy_updator():
    global proxy_object
    while True:
        if proxy_object.get_proxy_num()<10:
            print "当前线程数",threading.activeCount()
            print "正在添加代理",proxy_object.get_proxy_num()
            proxy_object.add_more_proxyip()#此线程陷入阻塞，但不影响其他线程对代理的获取
        else:
            #print "代理充足",proxy_object.get_proxy_num()
            sleep(1)

#负责拿到输入域名集
def domain_selector(domain_queue,select_handle):
    domains=select_handle()
    for domain in domains:
        domain_queue.put(domain)

#负责下载网页
def html_downloader(domain_queue,html_queue):
    while True:
        try:
            sleep(1)
            domain=domain_queue.get(timeout=config.get_domain_timeout)
            if config.enable_proxy:
                proxy=proxy_object.get_proxy()
            html=HtmlDownloader.html_downloader[config.to_download](domain,proxy)
            html_queue.put([domain,html])
            if config.enable_proxy:
                proxy_object.free_proxy(proxy)
        except Queue.Empty:
            return
        except Exception,e:
            #raise
            if config.enable_proxy:
                proxy_object.delete_proxy(proxy)
            html_queue.put([domain,""])

#负责解析网页，获取想要的数据
def html_parser(html_queue,result_queue,parser_handle):
    while True:
        data=""
        try:
            domain,html=html_queue.get(timeout=config.get_html_timeout)
            data=parser_handle(html)
            print "网页解析成功",domain,data
            result_queue.put([domain,data])
        except Queue.Empty:
            return
        except Exception,e:
            #print e
            result_queue.put([domain,data])

#负责提交分析的得到的数据
def result_commiter(result_queue,commit_handle):
    result=[]
    while True:
        try:
            result.append(result_queue.get(timeout=config.get_result_timeout))
        except Queue.Empty:
            commit_handle(result)
            return
        except Exception,e:
            raise

def _start_everything(select_handle,html_parse_handle,commit_handle):
    domain_queue=Queue.Queue()
    html_queue=Queue.Queue()
    data_queue=Queue.Queue()

    selecet_fun=lambda :domain_selector(domain_queue,select_handle)
    html_download_fun=lambda :html_downloader(domain_queue,html_queue)
    html_parse_fun=lambda :html_parser(html_queue,data_queue,html_parse_handle)
    commit_fun=lambda :result_commiter(data_queue,commit_handle)

    if config.enable_proxy:
        proxy_td=threading.Thread(target=proxy_updator)
    select_td=threading.Thread(target=selecet_fun)
    commit_td=threading.Thread(target=commit_fun)
    html_parse_td=threading.Thread(target=html_parse_fun)
    html_download_td=[]
    for _ in range(config.num_html_download_thread):
        html_download_td.append(threading.Thread(target=html_download_fun))
    if config.enable_proxy:
        proxy_td.start()
        sleep(config.init_proxy_timeout)
    select_td.start()
    for td in html_download_td:
        td.start()
    html_parse_td.start()
    commit_td.start()
    commit_td.join()

def start_everything(select_handle,html_handle,commit_handle):
    print "ok"
    for _ in range(3):
        _start_everything(select_handle,html_handle,commit_handle)
        # print "ok",i
    os._exit(0)

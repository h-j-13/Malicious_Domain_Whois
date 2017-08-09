# coding:utf-8

"""
    生产者消费者模型，通过传递函数来工作

    使用：
            在主函数中调用start_evrything(select_handle,html_handle,c
        ommit_handle,thread_num)
            要求满足：
            1.select_handle是函数对象，
                参数： 无
                返回值：select_handle()返回一个待查询的域名列表，
                说明：域名数量不限，建议为300
            2.html_handle是函数对象
                参数：一个html字符串对象
                返回值：html中的排名信息，int型
                说明：这个函数用于返回html中的排名信息，作为html解析函数
            3.commit_handle是函数对象
                参数：域名字符串和排名数字
                返回值：无
                说明：将域名的排名加入到数据库中
            4.thread_num是下载网页的线程数量，默认为5

    断言：
        1.可用代理ip在100秒内一定会有补充

    备注：
        domain_queue元素： 域名字符串
        temp_queue元素： [domain,html]
        result_queue元素： [domain,rank]
        实际情况中代理远远不够。
"""

import Queue
import threading
import urllib2
from time import sleep
from bs4 import BeautifulSoup
import word
import sys
reload(sys)
sys.setdefaultencoding('utf-8')




def download_htmlpage(domain, timeout):
    url = 'http://' + domain
    try:
        res = urllib2.urlopen(url)
        html = res.read()
        soup = BeautifulSoup(html, 'lxml')
        content = word.pre_deal(str(soup))
        # if content == '':
            # print '--------'
        return content
    except Exception, e:
        message = str(e)
        if message == '<urlopen error [Errno -5] No address associated with hostname>':
            # print '域名无关联地址 ...'
            return '-1'
        elif message == '<urlopen error [Errno 22] Invalid argument>':
            # print '域名错误 ... '
            return '-2'
        elif message == '<urlopen error timed out>':
            # print '请求超时 ...'
            return '-3'
        elif message == 'HTTP Error 400: Bad Request':
            # print 'HTTP 400错误 ...'
            return '-4'
        elif message == 'HTTP Error 502: Bad Gateway':
            # print 'HTTP 502错误 ...'
            return '-5'
        elif message == 'timed out':
           #  print '请求超时 ...'
            return '-3'
        elif message == '<urlopen error [Errno -3] Temporary failure in name resolution>':
            # print 'Wrong ...'
            return '-6'
        elif message == 'HTTP Error 404: Not Found':
            # print 'HTTP 404错误 ...'
            return '-8'
        elif message == '<urlopen error [Errno -2] Name or service not known>':
            # print 'HTTP 404错误 ...'
            return '-9'
        elif message == 'HTTP Error 403: Forbidden':
            return '-10' 
        else:
            return '-7'


#调用数据库查询函数，获取一定数量域名，填充到任务队列
def domain_selecter(domain_queue, select_handle):
    while True:
        if domain_queue.empty():
            domains = select_handle()
            for item in domains:
                domain_queue.put(item)
        else:
            sleep(1)


#下载网页，放入队列中
def html_downloader(domain_queue, temp_queue, timeout=100):
    global proxy_object
    domain = "empty.domain"
    while True:
        try:
            domain = domain_queue.get(timeout=timeout)
            content = download_htmlpage(domain=domain, timeout=3)
            temp_queue.put([domain, content])
        except WrongHtml, e:#下载任务未完成，放回任务队列
            domain_queue.put(domain)
        except Queue.Empty:
            return
        except Empytword_Geturl, e:
            print '------------------------------'
            print domain
            # 加入get_url 获取重定向后的url


#解析网页内容
def html_parser(temp_queue, result_queue, html_handle, timeout=300):
    while True:
        try:
            domain, content = temp_queue.get(timeout=timeout)
            if content == '-1' or content == '-2' or content == '-3' or content == '-4' or content == '-5' or content == '-6' or content == '-7':
                keywords = content
            else:
                keywords = html_handle(content)
                if keywords == '':
                    keywords = '--'
                    # print '关键词为空'
            print domain + '\tkeywords: ' + keywords
            result_queue.put([domain, keywords])
        except Queue.Empty:
            return


#将查询结果送入数据库
def add_to_db(result_queue, commit_handle, timeout=500):
    while True:
        try:
            domain, index = result_queue.get(timeout=timeout)
            commit_handle(domain, index)
        except Queue.Empty:
            return
        except OperationalError, e:
            pass
            continue


def start_evrything(select_handle,html_handle,commit_handle,thread_num=5):
    domain_queue = Queue.Queue()
    temp_queue = Queue.Queue()
    result_queue = Queue.Queue()

    selecet_fun=lambda :domain_selecter(domain_queue,select_handle)
    html_download_fun=lambda :html_downloader(domain_queue,temp_queue)
    html_parse_fun=lambda :html_parser(temp_queue,result_queue,html_handle)
    commit_fun=lambda :add_to_db(result_queue,commit_handle)

    select_td = threading.Thread(target=selecet_fun)
    commit_td = threading.Thread(target=commit_fun)
    html_parse_td = threading.Thread(target=html_parse_fun)
    html_download_td = []
    for _ in range(thread_num):
        html_download_td.append(threading.Thread(target=html_download_fun))
    select_td.start()
    for td in html_download_td:
        td.start()
    html_parse_td.start()
    commit_td.start()
    commit_td.join()

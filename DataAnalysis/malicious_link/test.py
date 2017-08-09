# -*- coding: UTF-8 -*-
import Queue
import MySQLdb
import threading
from time import sleep
import discover
import judge_mal
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

domain_title_q = Queue.Queue()
new_urls_q = Queue.Queue()
content_q = Queue.Queue()
res_q = Queue.Queue()
SE_thread_num = 10


def get_domains(flag):
	global domain_title_q
	flag = "'%" + str(flag) + "'"
	global keywors_q
	conn = MySQLdb.connect('172.26.253.3', 'root', 'platform', 'malicious_domain_sys', charset = 'utf8')
	cur = conn.cursor()
	# SQL = "SELECT domain, malicious_info.title FROM malicious_info, domain_index WHERE malicious_info.ID = domain_index.ID AND flag LIKE %s;" %flag
	SQL = "SELECT domain, malicious_info.title FROM malicious_info, domain_index WHERE malicious_info.ID = domain_index.ID AND flag LIKE %s;" %flag
	cur.execute(SQL)
	result = cur.fetchall()
	print result
	for item in result:
		 if item[0] != "771288.com" and item[0] != "jz-med.com" and item[0] != "6997789.com" and item[0] !="1055365.com" and item[0] !="606tk.com":
			domain_title_q.put([item[0], item[1]])
	print 'get domains ...'



def SE_get_urls_handle():
	global domain_title_q
	global new_urls_q
	while True:
		if domain_title_q.empty():
			break
		domain, title = domain_title_q.get()
		Baidu_urls = discover.Baidu_get_raw_html(domain, title)
		Bing_urls = discover.Bing_get_raw_html(domain, title)
		urls = Baidu_urls + Bing_urls
		urls = list(set(urls))
		for url in urls:
			new_urls_q.put('http://' + url)
	print 'SE get over ...'


def judge_download_handle():
	global new_urls_q
	global content_q
	while True:
		try:
			url = new_urls_q.get(timeout=100)
		except Queue.Empty:
			break
		url, content = judge_mal.download_htmlpage(url)
		if url != '':
			content_q.put([url, content])
	print 'judge_download over ...'


def judge_type_handle():
	global content_q
	global res_q
	while True:
		try:
			url, content = content_q.get(timeout=200)
		except Queue.Empty:
			break
		url, ttype = judge_mal.judge_url_type(url, content)
		res_q.put([url, ttype])
	print 'judge over ...'


conn = MySQLdb.connect('172.26.253.3', 'root', 'platform', 'keywords', charset= 'utf8')
cur = conn.cursor()
def save_result():
	global conn, cur
	global res_q
	while True:
		try:
			url, ttype = res_q.get(timeout=500)
		except Queue.Empty:
			break
		print url, ttype
		SQL = "REPLACE INTO SE_search (url,type) VALUES('" + url + "', '" + ttype + "')"
		cur.execute(SQL)
		conn.commit()
		print 'upset successfullly ...'
	cur.close()
	conn.close()
	print 'saved over ...'


if __name__ == '__main__':
	get_domains(1)
	SE_get_html_td = []
	sleep(10)
	# 搜索引擎获取url
	for _ in range(SE_thread_num):
		SE_get_html_td.append(threading.Thread(target=SE_get_urls_handle))
	for td in SE_get_html_td:
		td.start()
	sleep(10)
	judge_download_td = []
	for _ in range(SE_thread_num):
		judge_download_td.append(threading.Thread(target=judge_download_handle))
	for td in judge_download_td:
		td.start()
	sleep(20)
	judge_type_td = threading.Thread(target=judge_type_handle)
	judge_type_td.start()
	save_db_td = threading.Thread(target=save_result)
	save_db_td.start()
	save_db_td.join()

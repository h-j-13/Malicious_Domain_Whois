# -*- coding: UTF-8 -*-
'''
	功能： 从大库获取域名作为源头在搜索引擎中爬取链接
'''
import Queue
import requests
import MySQLdb
import threading
from time import sleep
from log import *
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


domain_q = Queue.Queue()
url_q = Queue.Queue()
SE_thread_num = 10

sites = ['bbs.', 'zhidao.baidu', 'weibo.com']

headers = {"Accept": "text/html;",
	            "Accept-Language": "zh-CN,zh;q=0.8",
	            "Referer": "http://www.baidu.com/",
	            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
	            }

# 根据flag获取某一类型的域名（问题是无法区分哪些是已经选取过的）
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
	for item in result:
		domain_q.put([item[0], item[1]])
	print 'get domains ...'


# 在 Baidu 和 Bing 爬取前200页的链接
def SE_get_raw_html():
	global url_q
	global domain_q
	while True:
		wd, title = domain_q.get()
		exact_wd = '"' + wd + '"'
		for wd in [exact_wd, title]:
			print wd
			if wd == '':
				continue
			sleep(1)
			for page in range(0, 200, 10):
				urls = []
				payload = {'wd': wd, 'pn': str(page)}
				for i in range(10):
					try:
						html = requests.get('https://www.baidu.com/baidu', params=payload, headers=headers, timeout=5).text
						break
					except:
						if i == 9:
							logger.info(wd)
						else:
							sleep(0.5)
				urls = urls + re.compile(r'<a target="_blank" href=".+?" class="c-showurl" style=".*?">([^>]+?)\/&nbsp;</a>').findall(html)
				payload = {'q': wd, 'go': 'Submit', 'first': str(page)}
				for i in range(10):
					try:
						html = requests.get('http://cn.bing.com/search', params=payload, headers=headers, timeout=5).text
						break
					except:
						if i == 9:
							logger.info(wd)
						sleep(0.5)
				print 'Bing ' + str(page)
				urls = urls + re.compile(r'<li class="b_algo"><h2><a target="_blank" href="http://(.+?)" h=".+?"').findall(html)	
				urls = list(set(urls))
				for url in urls:
					print 'put ...'
					url_q.put(url)


conn = MySQLdb.connect('172.26.253.3', 'root', 'platform', 'keywords', charset= 'utf8')
cur = conn.cursor()
def save_result():
	global conn, cur
	global url_q
	while True:
		try:
			url = url_q.get(timeout=500)
			print '--------------'
		except Queue.Empty:
			print '*********************'
			break
		print url
		SQL = "REPLACE INTO SE_search (url) VALUES('" + url + "')"
		cur.execute(SQL)
		conn.commit()
		print 'upset successfullly ...'
	cur.close()
	conn.close()
	print 'saved over ...'


if __name__ == '__main__':
	get_domains(1)
	SE_get_html_td = []
	for _ in range(SE_thread_num):
		SE_get_html_td.append(threading.Thread(target=SE_get_raw_html))
	for td in SE_get_html_td:
		td.start()
	sleep(10)
	print 'SAVE START ...'
	save_db_td = threading.Thread(target=save_result)
	save_db_td.start()
	save_db_td.join()

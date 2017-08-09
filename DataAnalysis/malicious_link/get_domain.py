# coding:utf-8
'''
	之前设计库的时候没有设计域名，此脚本将url进行域名提取
'''
from bs4 import BeautifulSoup
from time import sleep
from tld import get_tld
from log import *
import MySQLdb
import threading
import Queue


url_q = Queue.Queue()
res_q = Queue.Queue()
thread_num = 10


def get_urls():
	global url_q
	conn = MySQLdb.connect('172.26.253.3', 'root', 'platform', 'keywords', charset = 'utf8')
	cur = conn.cursor()
	SQL = "SELECT url FROM SE_search WHERE domain IS NULL LIMIT 30000;"
	cur.execute(SQL)
	result = cur.fetchall()
	for item in result:
		url_q.put(item[0])
	print 'get urls ...'



def get_domain():
	global url_q
	while True:
		if url_q.empty():
			break
		url = url_q.get()
		try:
			domain = str(get_tld(url))
		except:
			logger.info(url + 'get domian wrong ...')
			continue
		res_q.put([url, domain])
	print 'get domains over ...'



conn = MySQLdb.connect('172.26.253.3', 'root', 'platform', 'keywords', charset= 'utf8')
cur = conn.cursor()
def save_result():
	global conn, cur
	global res_q
	while True:
		try:
			url, domain = res_q.get(timeout=200)
			print url, domain
		except Queue.Empty:
			break
		SQL = "UPDATE SE_search SET domain = '" + domain + "' WHERE url = '" + url + "';"
		cur.execute(SQL)
		conn.commit()
		print 'upset successfullly ...'
	cur.close()
	conn.close()
	print 'saved over ...'


def run():
	get_urls()
	get_domain_td = []
	for _ in range(thread_num):
		get_domain_td.append(threading.Thread(target=get_domain))
	for td in get_domain_td:
		td.start()
	sleep(5)
	SQLdb_td = threading.Thread(target=save_result)
	SQLdb_td.start()
	SQLdb_td.join()


if __name__ == '__main__':
	run()

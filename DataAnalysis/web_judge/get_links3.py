# coding:utf-8
'''
	功能：
		填充 malicious_info 表中 malicious_link 内容以及 malicious_link 表中内容
'''
from bs4 import BeautifulSoup
from time import sleep
from tld import get_tld
from log import *
import urllib2
import MySQLdb
import socket
import chardet
import threading
socket.setdefaulttimeout(10)
import Queue
import db_operation
from time import sleep
from log import *


white_list = db_operation.white_list
black_list = db_operation.black_list  # 关于黑名单的问题是，如果日后黑名单量较大，在黑名单中比对效率问题
domain_q = db_operation.domain_q
soup_q = Queue.Queue()
res_q = Queue.Queue()
thread_num = 10


# urllib2获取响应可能存在压缩包问题，在此处理；同时处理编码问题
def pre_deal_html(req):
	info = req.info()
	content = req.read()
	encoding = info.getheader('Content-Encoding')
	if encoding == 'gzip':
		buf = StringIO(content)
		gf = gzip.GzipFile(fileobj=buf)
		content = gf.read()
	charset = chardet.detect(content)['encoding']
	if charset != 'utf-8' and charset != None:
		content = content.decode(charset, 'ignore')
	return content


def get_html():
	global url_q
	global soup_q
	while True:
		if domain_q.empty():
			break
		domain = domain_q.get()
		url = 'http://' + domain
		flag = False
		# 可能一次请求失败，请求五次，五次都失败则定义为请求异常入库
		for _ in range(5):
			try:
				resp = urllib2.urlopen(url)
				html = pre_deal_html(resp)
				flag = True  # 成功取回网页置flag为True
				break
			except Exception, e:
				continue
		if flag == False:  # flag 为False 说明五次均未取回网页
			res_q.put([domain, []])
			continue
		else:
			try:
				soup = BeautifulSoup(html, 'lxml')
				soup_q.put([domain, soup])
			except:
				print url + 'pre_deal 出现问题'
	print 'download over ...'


def judge_a_links():
	global white_list
	global balck_list
	global soup_q
	global res_q
	while True:
		try:
			domain, soup = soup_q.get(timeout=50)
		except Queue.Empty:
			break
		mal_urls = []
		for a in soup.find_all('a'):
			try:
				url = a['href']
				url_domain = get_tld(url)
				if url_domain != domain:  # 获取除本网站站内连接之外的链接
					if url_domain in black_list or url_domain not in white_list:
					# 目前先将不在白名单中域名url都放入malicious_link表内，待以后malicious_link表足够完全后，再只用黑名单
						mal_urls.append((url, url_domain))
			except Exception, e:
				# logger.info(domain + '   GET LINKS WRONG ...')
				continue
		res_q.put([domain, mal_urls])
	print 'links over ...'


conn = MySQLdb.connect('172.26.253.3', 'root', 'platform', 'malicious_domain_sys', charset = 'utf8')
cur = conn.cursor()
def save_db():
	global res_q
	global conn, cur
	while True:
		try:
			domain, mal_urls = res_q.get(timeout=150)
			print 'get ' + domain, mal_urls
		except Queue.Empty:
			break
		if mal_urls != []:
			string = ''
			try:
				for item in mal_urls:
					SQL_malicious_links = "REPLACE INTO malicious_link(url_id, url, url_domain) VALUES('" + str(hash(item[0])) + "', '" + item[0] + "' , '" + item[1] + "')"
					cur.execute(SQL_malicious_links)
					string = string + str(hash(item[0])) + ','
				string = string[:len(string) - 1]
				SQL = "UPDATE malicious_info SET malicious_link =  '" + string + "' WHERE ID = %s" %hash(str(domain))
				cur.execute(SQL)
				SQL = "UPDATE malicious_info SET flag =  flag + 10 WHERE ID = %s" %hash(str(domain))
				cur.execute(SQL)
				conn.commit()
			except Exception, e:
				logger.info(domain + str(e))
				continue
		else:  # 初始提取链接为空的情况
			SQL = "UPDATE malicious_info SET flag =  flag + 20 WHERE ID = %s" %hash(str(domain))
			cur.execute(SQL)
			conn.commit()
		print domain + '  saved successfully ...'
	cur.close()
	conn.close()
	print 'db over ...'



if __name__ == '__main__':
	get_html_td = []
	for _ in range(thread_num):
		get_html_td.append(threading.Thread(target=get_html))
	for td in get_html_td:
		td.start()
	sleep(10)
	judge_td = threading.Thread(target=judge_a_links)
	judge_td.start()
	SQLdb_td = threading.Thread(target=save_db)
	SQLdb_td.start()
	SQLdb_td.join()

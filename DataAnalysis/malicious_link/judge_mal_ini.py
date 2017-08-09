# coding:utf-8
'''
	功能：
		SE_search 表中 type 的判别 （ 0 未判断 1 赌博 2 色情 9 类型未知）

'''
from bs4 import BeautifulSoup
from time import sleep
import urllib2
import MySQLdb
import chardet
import threading
import Queue
import jieba.analyse
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import socket
socket.setdefaulttimeout(10)


lottery_words = open('../search_discover/赌博words.txt', 'r').readlines()
sexy_words = open('../search_discover/色情words.txt', 'r').readlines()
words_list = [lottery_words, sexy_words]
stop_list = ['的', '或', '是', '啦', '去' ,'也', '只', '而']

url_q = Queue.Queue()
res_q = Queue.Queue()
content_q = Queue.Queue()
thread_num = 1

def get_urls():
	global url_q
	conn = MySQLdb.connect('172.26.253.3', 'root', 'platform', 'keywords', charset = 'utf8')
	cur = conn.cursor()
	# SQL = "SELECT domain, malicious_info.title FROM malicious_info, domain_index WHERE malicious_info.ID = domain_index.ID AND flag LIKE %s;" %flag
	SQL = "SELECT url FROM SE_search WHERE type='0' LIMIT 10;"
	cur.execute(SQL)
	result = cur.fetchall()
	for item in result:
		url_q.put(item[0])
	print 'get urls ...'


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


# 提前中文内容,过滤字母特殊符号
def pre_deal(string):
	string = re.sub("[\A-Za-z0-9_\s+\.\!\/_,$%^*(+\"\']".decode("utf8"), "".decode("utf8"),string)
	string = re.sub("[+——！，。？、~@#￥%……&*（）：“”;【】?―:　-]".decode("utf8"), "".decode("utf8"),string)
	string = re.sub("[\{\}<>=)«|\[\]  ]".decode("utf8"), "".decode("utf8"),string)
	return string


def cut_string(string):
	global stop_list
	words = []
	seg_list = jieba.cut(string, cut_all=False)
	temp = ",".join(seg_list)
	temp = temp.split(',')
	for i in temp:
		if i not in stop_list:
			words.append(i)
	return words


def download_htmlpage():
	global url_q
	global content_q
	while True:
		if url_q.empty():
			break
		url = url_q.get()
		flag = False
		# 可能一次请求失败，请求五次，五次都失败则定义为请求异常入库
		for _ in range(5):
			try:
				resp = urllib2.urlopen(url)
				html = pre_deal_html(resp)
				flag = True #  成功取回网页置flag为True
				break
			except Exception, e:
				# print '-----'
				continue
		if flag == False: #  flag 为False 说明五次均未取回网页
			res_q.put([url, '8'])
			continue
		else:
			try:
				print html
				soup = BeautifulSoup(html, 'lxml')
				content = pre_deal(str(soup))
				content_q.put([url, content])
			except:
				print url + 'pre_deal 出现问题'
	print 'download over ...'



def judge_url_type():
	global content_q
	global res_q
	while True:
		try:
			url, content = content_q.get(timeout=20)
		except Queue.Empty:
			break
		if content == '':
			res_q.put([url, '9'])
		temp = []
		length = len(cut_string(content))
		for i in range(len(words_list)):
			words = words_list[i]
			num = 0
			count = 0
			for item in words:
				item = item.strip()
				if item in content:
					num = num + content.count(item)
					count = count + 1
			rate = num / length
			temp.append((count, rate))
		if temp[0][0] > temp[1][0]:
			ttype = '1'
			count = temp[0][0]
			rate = temp[0][1]
		else:
			ttype = '2'
			count = temp[1][0]
			rate = temp[1][1]
		if count > 3 or rate > 0.1:
			res_q.put([url, ttype])
		else:
			res_q.put([url, '9'])
	print 'judge over ...'


conn = MySQLdb.connect('172.26.253.3', 'root', 'platform', 'keywords', charset= 'utf8')
cur = conn.cursor()
def save_result():
	global conn, cur
	global res_q
	while True:
		try:
			url, ttype = res_q.get(timeout=2000)
		except Queue.Empty:
			break
		# SQL = "UPDATE SE_search SET type = '" + ttype + "' WHERE url = '" + url + "';"
		SQL = "REPLACE INTO SE_search (url, type) VALUES('" + url + "', '" + ttype + "');"
		cur.execute(SQL)
		conn.commit()
		print 'upset successfullly ...'
	cur.close()
	conn.close()
	print 'saved over ...'


if __name__ == '__main__':
	get_urls()
	get_html_td = []
	for _ in range(thread_num):
		get_html_td.append(threading.Thread(target=download_htmlpage))
	for td in get_html_td:
		td.start()
	sleep(10)
	judge_type_td = threading.Thread(target=judge_url_type)
	judge_type_td.start()
	sleep(5)
	# SQLdb_td = threading.Thread(target=save_result)
	# SQLdb_td.start()
	# SQLdb_td.join()
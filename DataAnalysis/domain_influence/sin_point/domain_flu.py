# -*- coding: UTF-8 -*-
import MySQLdb
import Queue
import threading
from time import sleep
import requests
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


domain_title_q = Queue.Queue()
res_q = Queue.Queue()

thread_num = 5
sites = ['bbs.', 'zhidao.baidu', 'weibo.com']

headers = {"Accept": "text/html;",
	            "Accept-Language": "zh-CN,zh;q=0.8",
	            "Referer": "http://www.baidu.com/",
	            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
	            }


# 选择时候的flag数值  (现在代表类型)
def get_domains(flag):
	global domain_title_q
	flag = "'%" + str(flag) + "'"
	global keywors_q
	conn = MySQLdb.connect('172.26.253.3', 'root', 'platform', 'malicious_domain_sys', charset = 'utf8')
	cur = conn.cursor()
	SQL = "SELECT domain, malicious_info.title FROM malicious_info, domain_index WHERE malicious_info.ID = domain_index.ID AND flag LIKE %s limit 100;" %flag
	cur.execute(SQL)
	result = cur.fetchall()
	for item in result:
		domain_title_q.put([item[0], item[1]])



def Baidu_get_raw_html(domain, title):
	wd_list = []
	wd_list.append(domain)
	wd_list.append('"' + domain + '"')
	if title != '':
		wd_list.append(title)
		wd_list.append('"' + title + '"')
	counts = []
	for item in wd_list:
		ini_payload = {'wd': item, 'pn': str(0)}
		try:
			ini_html = requests.get('https://www.baidu.com/s', params=ini_payload, headers=headers, timeout=5).text
			if '很抱歉，没有找到' in ini_html:
				counts.append(0)
				continue
			total_pages = re.compile(r'<div class="search_tool" ><i class="c-icon searchTool-spanner c-icon-setting"></i>.+?(</div>.+?</div>)</div></div>').findall(ini_html)[0].replace(',', '')
			total_pages = int(re.compile(r'</div>.*?(\d+).*</div>').findall(total_pages)[0])
			counts.append(total_pages)
		except:
			print domain, item
	print 'Baidu:', counts
	counts.sort()
	return counts[-1]


def Bing_get_raw_html(domain, title):
	wd_list = []
	wd_list.append(domain)
	wd_list.append('"' + domain + '"')
	if title != '':
		wd_list.append(title)
		wd_list.append('"' + title + '"')
	counts = []
	for item in wd_list:
		ini_payload = {'q': item, 'go': 'Submit', 'first': str(0)}
		try:
			ini_html = requests.get('http://cn.bing.com/search', params=ini_payload, headers=headers, timeout=5).text
			if '没有找到' in ini_html:
				counts.append(0)
				continue
			total_pages = int(re.compile(r'<span class="sb_count">(.+?)</span><span class="ftrB">').findall(ini_html)[0].split(' ')[0].replace(',', ''))
			counts.append(total_pages)
		except:
			print domain, item
	# counts[0]: 模糊匹配, counts[1]: 精确匹配
	print 'Bing', counts
	counts.sort()
	return counts[-1]


# 在百度和必应搜索各自搜索数量中取最大值，再在这两者之间取最大值作为影响力指数。
def get_domain_influ():
	global domain_title_q
	global res_q
	while True:
		if domain_title_q.empty():
			break
		domain, title = domain_title_q.get()
		Baidu_count = Baidu_get_raw_html(domain, title)
		Bing_count = Bing_get_raw_html(domain, title)
		count = max(Baidu_count, Bing_count)
		res_q.put([domain, count])
	print 'get domain influ ends ...'



conn = MySQLdb.connect('172.26.253.3', 'root', 'platform', 'malicious_domain_sys', charset = 'utf8')
cur = conn.cursor()
def commit_result():
	global conn, cur
	global res_q
	while True:
		try:
			domain, count = res_q.get(timeout=10)
		except Queue.Empty:
			break
		#  SQL = "REPLACE INTO malicious_info(ID, title, key_word, malicious_keywords, judge_grade) VALUES('" + str(hash(domain)) + "', '" + title + "', '" + keywords + "', '" + malicious_keywords + "' , '" + str(grade) + "')"
		try:
			print domain, count
			# SQL = "UPDATE malicious_info SET title='" + title + "', key_word='" + keywords + "', malicious_keywords='" + malicious_keywords + "', judge_grade=%s WHERE ID = %s" %(str(grade), str(hash(domain)))
			# SQL = "REPLACE INTO malicious_info(ID, title, key_word, malicious_keywords, judge_grade) VALUES('" + str(hash(domain)) + "', '" + title + "', '" + keywords + "', '" + malicious_keywords + "' , '" + str(grade) + "')"
			# cur.execute(SQL)
			# SQL = "UPDATE malicious_info SET flag = flag + %s WHERE ID = %s" %(str(flag), str(hash(domain)))
			# cur.execute(SQL)
			# conn.commit()
		except:
			# print domain
			continue
	# cur.close()
	# conn.close()
	print 'db over ...'


def run():
	global thread_num
	get_domains(1)
	get_influ_td = []
	for _ in range(thread_num):
		get_influ_td.append(threading.Thread(target=get_domain_influ))
	for td in get_influ_td:
		td.start()
	# sleep(20)
	# save_db_td = threading.Thread(target=commit_result)
	# save_db_td.start()
	# save_db_td.join()

if __name__ == '__main__':
	run()
	# get_domains(1)
	# title = '香港赛马会|www.08111.com|香港挂牌|香港六合彩|香港马会开奖结果|开奖结果|香港六合彩特码图库|曾道人|白小姐|惠泽社群|香港赛马会|六合彩开奖记录|'
	# domain = '388488.com'
	# Baidu_get_raw_html(domain, title)
	# Bing_get_raw_html(domain, title)
	# print get_domain_influ(domain, title)
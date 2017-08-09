# -*- coding: UTF-8 -*-
'''
	较之domain_flu，域名 和 标题 精确查询的数值都太少， 尤其是域名， 因此去除二者的精确查询
'''
import MySQLdb
import Queue
import threading
import requests
import re
import time
from log import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


domain_title_q = Queue.Queue()
res_q = Queue.Queue()

thread_num = 1


headers = {"Accept": "text/html;",
	            "Accept-Language": "zh-CN,zh;q=0.8",
	            "Referer": "http://www.baidu.com/",
	            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
	            }


# 选择时候的flag数值  (现在代表类型)
def get_domains():
	global domain_title_q
	global keywors_q
	conn = MySQLdb.connect('172.26.253.3', 'root', 'platform', 'malicious_domain_sys', charset = 'utf8')
	cur = conn.cursor()
	SQL = "SELECT domain, malicious_info.title FROM malicious_info, domain_index WHERE malicious_info.ID = domain_index.ID AND flag < 10000 limit 5000;"
	cur.execute(SQL)
	result = cur.fetchall()
	for item in result:
		domain_title_q.put([item[0], item[1]])
	print 'domains and titles got ...'


# 在这里对获取到的counts数组进行处理，如果只有域名查询数量的数据，则直接返回该数据即可;
# 若还有title查询的数据， 则对数据进行如下处理：0.8 * counts[0] + 0.2 * counts[1]， 即分别赋予其0.8 和 0.2 的权重进行计算
def data_handle(counts):
	if len(counts) == 1:
		return counts[0]
	else:
		index = 0.8 * counts[0] + 0.2 * counts[1]
		return index


def Baidu_get_raw_html(domain, title):
	wd_list = []
	wd_list.append(domain)
	if title != '':
		wd_list.append(title)
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
			logger.info('Baidu:' + domain + '\t' + item)
			return 0
	index = data_handle(counts)
	return index


def Bing_get_raw_html(domain, title):
	wd_list = []
	wd_list.append(domain)
	if title != '':
		wd_list.append(title)
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
			logger.info('Bing:' + domain + '\t' + item)
			return 0
	index = data_handle(counts)
	return index


# 根据data_handle获取到baidu 和 bing 的查询结果，再在这两者之间取最大值作为影响力指数。
def get_domain_influ():
	global domain_title_q
	global res_q
	while True:
		if domain_title_q.empty():
			break
		domain, title = domain_title_q.get()
		Baidu_index = Baidu_get_raw_html(domain, title)
		Bing_index = Bing_get_raw_html(domain, title)
		count = max(Baidu_index, Bing_index)
		date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
		res_q.put([domain, count, date])
	print 'get domain influ ends ...'



conn = MySQLdb.connect('172.26.253.3', 'root', 'platform', 'malicious_domain_sys', charset = 'utf8')
cur = conn.cursor()
def commit_result():
	global conn, cur
	global res_q
	while True:
		try:
			domain, count, date = res_q.get(timeout=10)
		except Queue.Empty:
			break
		# try:
		print domain, count, date
		SQL = "UPDATE malicious_info SET influence='" + str(count) + "', influence_last_update='" + date + "' WHERE ID = %s" %str(hash(domain))
		cur.execute(SQL)
		SQL = "UPDATE malicious_info SET flag = flag + 10000 WHERE ID = %s" %str(hash(domain))
		cur.execute(SQL)
		conn.commit()
		# except:
			# print domain
			# logger.info(domain + "MySQL save wrong ...")
			# continue
	cur.close()
	conn.close()
	print 'db over ...'


def run():
	global thread_num
	get_domains()
	get_influ_td = []
	for _ in range(thread_num):
		get_influ_td.append(threading.Thread(target=get_domain_influ))
	for td in get_influ_td:
		td.start()
	time.sleep(10)
	save_db_td = threading.Thread(target=commit_result)
	save_db_td.start()
	save_db_td.join()

if __name__ == '__main__':
	run()
	# get_domains(1)
	# title = '香港赛马会|www.08111.com|香港挂牌|香港六合彩|香港马会开奖结果|开奖结果|香港六合彩特码图库|曾道人|白小姐|惠泽社群|香港赛马会|六合彩开奖记录|'
	# domain = '388488.com'
	# Baidu_get_raw_html(domain, title)
	# Bing_get_raw_html(domain, title)
	# print get_domain_influ(domain, title)
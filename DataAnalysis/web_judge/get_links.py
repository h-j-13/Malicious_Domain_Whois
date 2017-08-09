# coding:utf-8
from bs4 import BeautifulSoup
import urllib2
from pyvirtualdisplay import Display
from selenium import webdriver
import selenium
from tld import get_tld
import MySQLdb
import requests


headers = {     "Accept-Language": "zh-CN,zh;q=0.8",
	            "Referer": "http://www.baidu.com/",
	            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
	            }


def get_whitelist():
	file = open('white_list.txt', 'r')
	whitelist = file.read().split('\n')
	file.close()
	return whitelist


def get_domains():
	conn = MySQLdb.connect("172.26.253.3", "root", "platform", "malicious_domain_sys")
	cur = conn.cursor()
	SQL = "select domain from domain_index, malicious_info where domain_index.ID = malicious_info.ID and state = '1';"
	cur.execute(SQL)
	result = cur.fetchall()
	domains = []
	for item in result:
		domains.append(item[0])
	print "domains got !\n"
	print domains
	return domains


def get_final_url(url):
	with Display(backend="xvfb", size=(1440, 900)):
		driver = webdriver.Chrome()
		driver.maximize_window()
		driver.get(url)
		url = driver.current_url
		driver.quit()
		return url


def get_a_links(url, white_list):
	try:
		source_domain = get_tld(url)
	except Exception, e:
		# print str(e)
		return {}
	a_links = {}
	try:
		html = urllib2.urlopen(url).read()
		soup = BeautifulSoup(html)
	except Exception, e:
		# print str(e)
		return {}
	for a in soup.find_all('a'):
		try:
			u = a['href']
			domain = get_tld(a['href'])
			if domain not in white_list and domain != source_domain:
				a_links[u] = domain
		except Exception, e:
			# print str(e)
			pass
	return a_links


if __name__ == '__main__':
	white_list = get_whitelist()
	# domains = get_domains()
	domains = ['0000zs.com', '0006808.com', '00101.net', '001kj.com', '0032006.com', '0032008.com', '005388.com', '0055076.com', '006677.com', '006958.com', '007zb.com', '0082.cc', '00aakk.com', '010-65856606.net', '012k.com', '012v.com', '017799.com', '01861.com', '020620.com', '021900.com']
	# domains = ['005388.com']
	string = ''
	for domain in domains:
		url = 'http://' + domain
		links = get_a_links(url, white_list)
		string = string + domain + '\n'
		print domain
		for key in links.keys():
			print key
			string = string + key + '\n'
		print '------------------\n'
		string = string + '--------------------------\n\n'
	w_file = open('demo', 'w')
	w_file.write(string)
	w_file.close()

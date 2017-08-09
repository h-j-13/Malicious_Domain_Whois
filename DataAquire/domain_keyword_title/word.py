
# -*- coding: UTF-8 -*-
'''
	功能： 
		1.获取源代码存储为n.txt, 用于 fenci.py 时直接测试用;
		2.对源代码预处理提取中文内容， 用于 tfidf_top.py 中提取分词使用;
'''
import urllib2
from bs4 import BeautifulSoup
import re
import socket
import requests
socket.setdefaulttimeout(10)
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def pre_deal(string):
	string = re.sub("[\A-Za-z0-9_\s+\.\!\/_,$%^*(+\"\']".decode("utf8"), "".decode("utf8"),string)
	string = re.sub("[+——！，。？、~@#￥%……&*（）：“”;【】?―:　-]".decode("utf8"), "".decode("utf8"),string)
	string = re.sub("[\{\}<>=)«|\[\]  ]".decode("utf8"), "".decode("utf8"),string)
	return string


def save_html(name, soup):
	string = str(soup)
	# string = pre_deal(string)
	w_file = open('../fenci/code/2_' + name + '.txt', 'w')
 	w_file.write(string)
	w_file.close()


def save_contents(name,string):
	w_file = open('../fenci/code/words_2_' + name + '.txt', 'w')
 	w_file.write(string)
	w_file.close()


if __name__ == '__main__':
	# lines = open('url4', 'r').readlines()
	# print lines
	lines = ['www.807111.com/#3428']
	i = 33333
	for domain in lines:
		string = ''
		url = 'http://' + domain.strip()
		try:
			html = urllib2.urlopen(url).read()
			soup = BeautifulSoup(html, 'lxml')
		except socket.timeout, e:
			print url
			print "socket timeout"
			continue
		except Exception, e:
			print url
			print e.message
			continue
		# save_html(str(i), soup)
		string = pre_deal(str(soup))
		save_contents(str(i),string)
		i = i + 1

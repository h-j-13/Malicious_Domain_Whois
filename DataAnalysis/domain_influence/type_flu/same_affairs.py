# -*- coding: UTF-8 -*-
import requests
import re
import Queue
import MySQLdb
from tld import get_tld
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


headers = {"Accept": "text/html;",
	            "Accept-Language": "zh-CN,zh;q=0.8",
	            "Referer": "http://www.baidu.com/",
	            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
	            }



def get_keywords(flag):
	flag = "'%" + str(flag) + "'"
	keywords = []
	conn = MySQLdb.connect('172.26.253.3', 'root', 'platform', 'malicious_domain_sys', charset = 'utf8')
	cur = conn.cursor()
	SQL = "SELECT key_word FROM malicious_info WHERE flag LIKE %s AND title != '';" %flag
	# SQL = "SELECT malicious_keywords FROM malicious_info WHERE flag LIKE %s AND title != '';" %flag
	# print SQL
	cur.execute(SQL)
	result = cur.fetchall()
	for item in result:
		keywords.append(item[0])
	return keywords


def get_top10_keywords(flag):
	keywords = get_keywords(flag)
	keywords = ','.join(keywords)
	keywords = keywords.split(',')
	words_count = {}
	for word in keywords:
		words_count[word] = keywords.count(word)
	words_count = sorted(words_count.items(), key=lambda words_count:words_count[1], reverse = True)
	wd = []
	for i in range(10):
		# print words_count[i][0], words_count[i][1]
		wd.append(words_count[i][0])
	return wd


if __name__ == '__main__':
	# get_keywords(2)
	get_top10_keywords(2)

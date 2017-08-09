# -*- coding: UTF-8 -*-
from __future__ import division 
import requests
import MySQLdb
import re
import same_affairs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


headers = {"Accept": "text/html;",
	            "Accept-Language": "zh-CN,zh;q=0.8",
	            "Referer": "http://www.baidu.com/",
	            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
	            }


beginDate = '2017-03-20'
endDate = '2017-04-21'
days = 30
flag = 1
keywords = same_affairs.get_top10_keywords(flag)
print keywords



# 从网络获取raw_data
def get_raw_data(q_word):
	global beginDate
	global endDate
	print q_word
	payload = {'type': '0', 'beginDate': beginDate, 'endDate': endDate, 'cityid': '0', 'kw': q_word, 'apikey': 'W2KZDXt6AWyadYnEWibEZuBITUImhzBjzn5oV6NuykKm5R5U8k9YtKbBgPU2g2mA'}
	raw_data = requests.get('http://api01.bitspaceman.com:8000/kwindex/baiduindex?', params=payload, headers=headers, timeout=5).text
	return raw_data


# 以后这里改成输入为网络获取的raw_data
def get_values(raw_data):
	data = str(re.compile(r'"overallDist"(.+?)"cityDist"').findall(raw_data))
	values = re.compile(r'"value": ([\d]+?)\}').findall(data)
	return values


# 获取一个月来每天的数值，返回列表
def get_month_values():
	global keywords
	month_total_values = []
	for q_word in keywords:
		raw_data = get_raw_data(q_word)
		values = get_values(str(raw_data))
		if values != []:
			month_total_values.append(values)
	words_num = len(month_total_values)  # words_num统计实际查询到指数的词的个数
	month_values = []
	for day in range(days):
		day_value = 0
		# 计算方法：对每天的10个次求平均值得到每天value, 再对30天求均值
		for item in month_total_values:
			day_value = day_value + int(item[day])
		day_value = day_value / words_num
		month_values.append(str(day_value))
		# print "day: " + str(day + 1) + '\t' + str(day_value)
	print month_values
	return month_values



def commit_res(month_values):
	global flag
	month_values = ','.join(month_values)
	conn = MySQLdb.connect('172.26.253.3', 'root', 'platform', 'malicious_domain_sys', charset = 'utf8')
	cur = conn.cursor()
	SQL = "UPDATE malicious_type SET tend_avg =  '" + month_values + "', start_date =  '" + beginDate + "', end_date =  '" + endDate + "' WHERE id = '%s'" %flag
	cur.execute(SQL)
	conn.commit()
	cur.close()
	conn.close()
	print 'saved over ...'


if __name__ == '__main__':
	# # 运行前在全居变量处声明flag和起始日期
	month_values = get_month_values()
	commit_res(month_values)

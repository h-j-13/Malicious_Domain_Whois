# -*- coding: UTF-8 -*-
from __future__ import division 
import requests
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

words_num = 10
# q_word_lottery = ['澳门', '开奖', '娱乐场', '金沙', '六合彩', '香港', '娱乐城', '葡京', '博彩', '投注']
# q_word_lottery = ['娱乐','投注', '澳门', '葡京', '赌场', '博彩', '香港', '金沙', '开奖', '六合'] # malicious_keywords
# q_word_sex = ['偷拍','影视','视频', '写真', '自拍', '减肥', '在线电影', '下载', '手机', '插件'] # keywords
# q_word_sex = ['视频','美女','自拍', '成人', '高清', '性爱', '色情', '丝袜', '写真', '人妻'] # malicious_keywords
beginDate = '2017-03-06'
endDate = '2017-04-06'
days = 30
flag = 2
keywords = same_affairs.get_top10_keywords(flag)



# 从网络获取raw_data
def get_raw_data():
	for q_word in q_word_lottery:
		print q_word
		payload = {'type': '0', 'beginDate': beginDate, 'endDate': endDate, 'cityid': '0', 'kw': q_word, 'apikey': 'W2KZDXt6AWyadYnEWibEZuBITUImhzBjzn5oV6NuykKm5R5U8k9YtKbBgPU2g2mA'}
		raw_data = requests.get('http://120.76.205.241:8000/kwindex/baiduindex?', params=payload, headers=headers, timeout=5).text
		file = open('../type_flu/q_words_index/' + q_word + '.txt', 'w')
		raw_data = file.write(raw_data)
		file.close()


# 以后这里改成输入为网络获取的raw_data
def get_values(q_word):
	file = open('../type_flu/q_words_index/' + q_word + '.txt', 'r')
	raw_data = file.read()  # 即为网络获取的raw_data
	file.close()
	data = str(re.compile(r'"overallDist"(.+?)"cityDist"').findall(raw_data))
	values = re.compile(r'"value": ([\d]+?)\}').findall(data)
	return values


# 计算方法：首先计算10个关键词各自30天均值，再把这30个均值相加求10个词的均值
def word_days_value():
	total_index = 0
	for q_word in q_word_lottery:
		total = 0
		values = get_values(q_word)
		for num in values:
			total = total + int(num)
		index = total / len(values)
		total_index = total_index + index
		print q_word, str(index)
	print 'overrall_index: ' + str(total_index / words_num)


# 计算方法：对每天的10个次求平均值得到每天value, 再对30天求均值
def day_montn_value():
	month_total_values = []
	for q_word in q_word_lottery:
		values = get_values(q_word)
		month_total_values.append(values)
	month_values = []
	for day in range(days):
		day_value = 0
		for item in month_total_values:
			day_value = day_value + int(item[day])
		day_value = day_value / words_num
		month_values.append(day_value)
		# print "day: " + str(day + 1) + '\t' + str(day_value)
	return month_values


if __name__ == '__main__':
	# get_raw_data()
	# word_days_value()
	day_montn_value()

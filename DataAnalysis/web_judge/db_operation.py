# coding:utf-8
import MySQLdb
import Queue



def get_whitelist():
	file = open('white_list', 'r')
	whitelist = file.read().split('\n')
	file.close()
	return whitelist


# 关于黑名单的问题是，如果日后黑名单量较大，在黑名单中比对效率问题
def get_blacklist():
	conn = MySQLdb.connect('172.26.253.3', 'root', 'platform', 'malicious_domain_sys', charset = 'utf8')
	cur = conn.cursor()
	SQL = "SELECT DISTINCT url_domain FROM malicious_link WHERE type = '2' or type = '1';"
	cur.execute(SQL)
	result = cur.fetchall()
	blacklist = []
	for item in result:
		blacklist.append(item[0])
	return blacklist


def get_domains():
	domain_q = Queue.Queue()
	conn = MySQLdb.connect("172.26.253.3", "root", "platform", "malicious_domain_sys")
	cur = conn.cursor()
	SQL = "update malicious_info set flag = flag + 20 where flag not like '%2_' and flag not like '%1_' and flag like '%8'"
	cur.execute(SQL)
	conn.commit()
	print 'update over ...'
	SQL = "select domain_index.domain from domain_index, malicious_info where domain_index.ID = malicious_info.ID and malicious_info.flag not like '%2_' and malicious_info.flag not like '%1_';"
	cur.execute(SQL)
	result = cur.fetchall()
	for item in result:
		domain_q.put(item[0])
	return domain_q
	print "domains got !\n"


domain_q = Queue.Queue()
white_list = get_whitelist()
black_list = get_blacklist()
domain_q = get_domains()

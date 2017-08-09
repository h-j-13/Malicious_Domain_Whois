# coding:utf-8
'''
功能：
    填充malicious_info表中
    ID, title, key_words, malicious_keywords, judge_grade,flag最后一位
    （1 赌博，2 色情， 8 请求失败， 9 无法分类）
    大体同judge3.py, 但所添加了对Urllib请求到压缩包的处理，见pre_deal_html(req)


'''
from __future__ import division
from bs4 import BeautifulSoup
from time import sleep
import urllib2
import MySQLdb
import threading
import Queue
import chardet
import jieba.analyse
import word
import fenci
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


lottery_words = open('../fenci/fenci_res/words/赌博words.txt', 'r').readlines()
sexy_words = open('../fenci/fenci_res/words/色情words.txt', 'r').readlines()
words_list = [lottery_words, sexy_words]

domain_q = Queue.Queue()
content_q = Queue.Queue()
res_q = Queue.Queue()
thread_num = 10

# 在这里确定恶意域名的ID集合，目前是 judge_flag为2或3
Select_mal_domain = "(SELECT ID FROM domain_index WHERE judge_flag = '2' or judge_flag = '3')"

def get_domains():
    global domain_q
    conn = MySQLdb.connect("172.26.253.3", "root", "platform", "malicious_domain_sys")
    cur = conn.cursor()
    SQL = "SELECT domain FROM domain_index,malicious_info WHERE malicious_info.ID = domain_index.ID AND malicious_info_flag LIKE '%0' LIMIT 2000"
    # domain_index.malicious_info_flag个位为0的域名即为malicious_info.flag个位为0的域名
    cur.execute(SQL)
    result = cur.fetchall()
    for item in result:
        domain_q.put(item[0])
    print "domains got !\n"



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



def download_htmlpage():
    global domain_q
    global content_q
    global res_q
    while True:
        if domain_q.empty():
            break
        domain = domain_q.get()
        url = 'http://' + domain
        print url
        try:
            resp = urllib2.urlopen(url)
            html = pre_deal_html(resp)
            soup = BeautifulSoup(html, 'lxml')
            content = word.pre_deal(str(soup))
            if content == '':
                res_q.put([domain, '', '', '', '0', 9])
            content_q.put([domain, soup])
        except Exception, e:
            res_q.put([domain, '', '', '', '0', 8])
    print 'download over ...'



def get_title(soup):
	if soup.title != None:
	    if soup.title.string != None:
	        title = soup.title.string.replace('\n', '').replace(' ', '')
	    else:
	    	title = ''
	else:
	    title = ''
	return title


def judge_type():
    global content_q
    while True:
        res = []
        try:
            domain, soup = content_q.get(timeout=100)
        except Queue.Empty:
            break
        title = get_title(soup)
        content = str(soup)
        content = word.pre_deal(content)
        keywords = jieba.analyse.extract_tags(content, topK=5)
        keywords = str(','.join(keywords))
        length = len(fenci.cut_string(content))
        for i in range(len(words_list)):
            words = words_list[i]
            num = 0
            count = 0
            theme_words = []
            for item in words:
                item = item.strip()
                if item in content:
                    theme_words.append(item)
                    num = num + content.count(item)
                    count = count + 1
            rate = num / length
            malicious_keywords = ','.join(theme_words)
            res.append((count, rate, malicious_keywords))
        # 赌博 0/色情 1, res[][0]: count, res[][1]: rate, res[][2]: malicious_keywords
        if res[0][0] > res[1][0]:
            judge_grade(domain, title, 1, keywords, res[0][0], res[0][1], res[0][2])
        else:
            judge_grade(domain, title, 2, keywords, res[1][0], res[1][1], res[1][2])


# domain, state, title, ttype, keywords, count, rate, malicious_keywords
def judge_grade(domain, title, flag, keywords, count, rate, malicious_keywords):
    global res_q
    if count > 4 and rate > 0.1:
        grade = 2
        # 确定是博彩/色情网站，存储相应分数和malicious_keywords
    elif count > 4:
        grade = 1
        # 可能博彩/色情网站，存储相应分数和malicious_keywords
    elif rate > 0.1:
        grade = 1
        # 可能博彩/色情网站，存储相应分数和malicious_keywords
    else:
        grade = 0
        flag = 9
    res_q.put([domain, title, keywords, malicious_keywords, grade, flag])





conn = MySQLdb.connect('172.26.253.3', 'root', 'platform', 'malicious_domain_sys', charset = 'utf8')
cur = conn.cursor()
def commit_result():
    global conn, cur
    global res_q
    while True:
        try:
            domain, title, keywords, malicious_keywords, grade, flag = res_q.get(timeout=100)
        except Queue.Empty:
            break
       #  SQL = "REPLACE INTO malicious_info(ID, title, key_word, malicious_keywords, judge_grade) VALUES('" + str(hash(domain)) + "', '" + title + "', '" + keywords + "', '" + malicious_keywords + "' , '" + str(grade) + "')"
        try:
            # SQL = "UPDATE malicious_info SET title='" + title + "', key_word='" + keywords + "', malicious_keywords='" + malicious_keywords + "', judge_grade=%s WHERE ID = %s" %(str(grade), str(hash(domain)))
            SQL = "REPLACE INTO malicious_info(ID, title, key_word, malicious_keywords, judge_grade) VALUES('" + str(hash(domain)) + "', '" + title + "', '" + keywords + "', '" + malicious_keywords + "' , '" + str(grade) + "')"
            cur.execute(SQL)
            SQL = "UPDATE malicious_info SET flag = flag + %s WHERE ID = %s" %(str(flag), str(hash(domain)))
            cur.execute(SQL)
            conn.commit()
        except:
            print domain
            continue
    cur.close()
    conn.close()
    print 'db over ...'



def start_evrything():
    get_domains()
    get_html_td = []
    for _ in range(thread_num):
        get_html_td.append(threading.Thread(target=download_htmlpage))
    for td in get_html_td:
        td.start()
    sleep(5)
    html_deal_td = threading.Thread(target=judge_type)
    html_deal_td.start()
    save_db_td = threading.Thread(target=commit_result)
    save_db_td.start()
    save_db_td.join()




if __name__ == '__main__':
    start_evrything()
    # get_domains()

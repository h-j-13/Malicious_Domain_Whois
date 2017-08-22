# coding:utf-8

from bs4 import BeautifulSoup
import SpiderEntry
import MySQLdb
import re
import time

def select_domain():
    #return ["www.baidu.com","www.qq.com"]
    conn=MySQLdb.connect("172.26.253.3", "root", "platform", "malicious_domain_sys")
    cur=conn.cursor()
    cur.execute("SELECT domain_index.domain FROM domain_index WHERE domain_index.ID NOT IN (SELECT other_info.ID FROM other_info) LIMIT 200;")
    result=cur.fetchall()
    domains=[]
    for item in result:
        domains.append(item[0])
    print domains
    return domains

def parse_alex_rank_html(html):
    if html=="":
        return "nill"
    if "非法的内容" in html:
        return "-1"
    if "非法字符" in html:
        return "0"
    else:
        soup=BeautifulSoup(html)
        for ul in soup.find_all('ul',{'class':'result_top'}):
            if len(ul['class'])==1:
                rank=ul.find_all('li')[5].string
                return rank

def commit_rank(result):
    print "提交数据 进行中"
    conn=MySQLdb.connect("172.26.253.3","root","platform","malicious_domain_sys")
    cur=conn.cursor()
    for item in result:
        try:
            print item,len(result)
            domain=item[0]
            rank=item[1]
            if rank=="nill":
                continue
            date = time.strftime("%Y-%m-%d", time.localtime())
            cur.execute("REPLACE INTO other_info(ID, Alex, Alex_last_update) VALUES('" + str(hash(domain)) + "' , '" + rank + "', '" + date + "')")
            # conn.commit()
            print "..."
            cur.execute("UPDATE other_info SET flag = 0 where ID = %s" % str(hash(domain)) )
            # conn.commit()
            print "---"
            cur.execute("UPDATE domain_index SET other_info_flag = other_info_flag + 100 where ID = %s" % str(hash(domain)))
            # conn.commit()
            print "+++"
        except Exception,e:
            print e
    conn.commit()
    print "提交数据 完成"

SpiderEntry.start_everything(select_domain,parse_alex_rank_html,commit_rank)

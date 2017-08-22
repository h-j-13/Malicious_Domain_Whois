# coding:utf-8

from bs4 import BeautifulSoup
import SpiderEntry
import MySQLdb
import re
import os
import time

def select_domain():
    #return ["www.baidu.com","www.qq.com"]
    conn=MySQLdb.connect("172.26.253.3", "root", "platform", "malicious_domain_sys")
    cur=conn.cursor()
    #cur.execute("SELECT domain_index.domain FROM domain_index WHERE domain_index.ID NOT IN (SELECT other_info.ID FROM other_info) LIMIT 100;")
    cur.execute("SELECT domain_index.domain FROM domain_index  where judge_flag=5 or judge_flag=-1 or judge_flag=-10 limit 300;")
    result=cur.fetchall()
    domains=[]
    for item in result:
        domains.append(item[0])
    print domains
    return domains

def parse_alex_rank_html(html):
    if html=="":
        print "请求发生错误"
        return -1
    pattern=re.compile(r"var.str.=.{(.*?)};")
    result=re.findall(pattern,html)[0]
    if result.find('webstate\":0')!=-1:
        print "安全"
        return 1
    elif result.find('"xujia":{"level":1')!=-1:
        print "虚假"
        return 2
    elif result.find('"guama":{"level":1')!=-1:
        print "挂码"
        return 3
    elif result.find('webstate\":4')!=-1:
        print "未知"
        return 4
    else:#有漏洞但是没有恶意内容，视为安全
        print "未检测到恶意内容"
        return 1

def commit_rank(result):
    print "提交数据 进行中"
    conn=MySQLdb.connect("172.26.253.3","root","platform","malicious_domain_sys")
    cur=conn.cursor()
    sql="UPDATE domain_index SET judge_flag=%s where domain=\"%s\""
    f=open("data.txt",'a')
    for item in result:
        print item
        domain=item[0]
        judge_flag=item[1]
        if judge_flag=="":
            continue
        # f.write(domain+" "+str(judge_flag))
        s=sql%(judge_flag,domain)
        print s
        cur.execute(s)
    conn.commit()
    print "提交数据 完成"

SpiderEntry.start_everything(select_domain,parse_alex_rank_html,commit_rank)
print "over"
os._exit(0)

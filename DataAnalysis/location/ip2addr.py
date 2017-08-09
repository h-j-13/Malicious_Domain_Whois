#coding=utf-8
import DNS
import sys
import MySQLdb
import time
import urllib2
import threading
import socket
import random
sys.path.append("./ip2region/binding/python")
from ip2Region import Ip2Region

reload(sys)
sys.setdefaultencoding('utf-8')

lock0 = threading.Lock()
lock1 = threading.Lock()
threads = []
dnslist = [['114.114.114.114'], ['114.114.115.115'], ['223.5.5.5'], ['223.6.6.6'], ['180.76.76.76'], ['1.2.4.8'], ['119.29.29.29'], ['182.254.116.116'], ['123.125.81.6'], ['140.207.198.6'], ['208.67.222.222'], ['208.67.220.220'], ['101.226.4.6']]

dbFile    = './ip2region/data/ip2region.db'
method    = 1
algorithm = "b-tree"

searcher = Ip2Region(dbFile)



def gethttpcode():
    conn = MySQLdb.connect(	
        host ='172.26.253.3',
        port = 3306,
        user ='root',
        passwd ='platform'
    )
    conn.set_character_set('utf8')
    cur = conn.cursor()
    cur.execute("SET NAMES utf8")
    cur.execute("use malicious_domain_sys;")
    conn.commit()
    i = 0
    while 1==1:
        ip_addr = ''
        ip_cn = ''
        flag = 1
        domain = ''
        if lock0.acquire():
            try:#取出一个域名
                domain = result.pop()[0]
                lock0.release()
            except:#域名池为空
                print "return"
                lock0.release()
                cur.close()
                conn.commit()
                conn.close()
                return
        n = random.randint(0,len(dnslist)-1)
        DNS.defaults['server'] = dnslist[n]
        #print domain + "\t" + DNS.defaults['server'][0]
        reqobj = DNS.Request()
        try:
            answerobj = reqobj.req(name = domain, qtype = DNS.Type.A)
            if not len(answerobj.answers):
                flag = -2
        except:
            flag = -1
        if flag > 0:
            try:
                for ip in answerobj.answers:
                    #print ip['data']
                    if not searcher.isip(ip['data']):
                        ip_cn += ','
                    else:

                        ip_cn_data = searcher.btreeSearch(ip['data'])
                        ip_cn = ip_cn + ip_cn_data["region"] + ','
                        #print ip_cn_data["region"]
                    ip_addr = ip_addr + ip['data'] + ','
                ip_addr = ip_addr[:-1]
                ip_cn = ip_cn[:-1]
                #print ip_addr,ip_cn
                cur.execute("UPDATE locate SET ip = '%s', ip_info = '%s' WHERE id = %d" % (ip_addr, ip_cn, hash(domain)))

            except MySQLdb.Error, e:
                print e
        if ip_cn == '':
            if ip_addr == '':
                flag = 3
            else:
                flag = 2
        else:
            flag = 1
        cur.execute("UPDATE locate SET flag=(flag div 100)*100 + %d * 10 + mod(flag, 10) WHERE id = %d" % (flag, hash(domain)))
        conn.commit()
        #print flag



if __name__ == "__main__":
    #start = datetime.datetime.now()
    socket.setdefaulttimeout(10)
    conn = MySQLdb.connect(	
            host ='172.26.253.3',
            port = 3306,
            user ='root',
            passwd ='platform'
        )
    conn.set_character_set('utf8')
    cur = conn.cursor()
    cur.execute("SET NAMES utf8")
    cur.execute("use malicious_domain_sys;")
    conn.commit()
    ncount = cur.execute("SELECT domain_index.domain FROM locate LEFT JOIN domain_index ON locate.id = domain_index.id WHERE locate.flag > 0 AND locate.flag mod 100 < 10")
    print ncount
    global result
    result  = list(cur.fetchall())
    cur.close()
    conn.close()
    i = 10
    while i > 0:
        th = threading.Thread(target = gethttpcode)
        threads.append(th)
        i -= 1
    for th in threads:
        th.setDaemon(True)
        th.start()
    for th in threads:
        th.join()
    print "over"














'''
# -*- coding: utf-8 -*-
import urllib
import urllib2
import sys
import DNS
import MySQLdb
import re
import random
reload(sys)
sys.setdefaultencoding('utf-8')

domain = ''
dnslist = [['114.114.114.114'], ['114.114.115.115'], ['223.5.5.5'], ['223.6.6.6'], ['180.76.76.76'], ['1.2.4.8'], ['119.29.29.29'], ['182.254.116.116'], ['8.8.8.8'], ['8.8.4.4'], ['208.67.222.222'], ['208.67.220.220'], ['101.226.4.6']]
n = 0

conn = MySQLdb.connect(	
        host ='172.26.253.3',
        port = 3306,
        user ='root',
        passwd ='platform'
    )
conn.set_character_set('utf8')
cur = conn.cursor()
cur.execute("SET NAMES utf8")
cur.execute("use zgx;")
conn.commit()

DNS.DiscoverNameServers()

cur.execute("select domain from domains LIMIT 1000")
result = cur.fetchall()

for domain in result:
    DNS.defaults['server'] = dnslist[n] 
    n = random.randint(0,len(dnslist)-1)
    print domain[0] + "\t" + DNS.defaults['server'][0]
    reqobj = DNS.Request()
    try:
        answerobj = reqobj.req(name = domain[0], qtype = DNS.Type.A)
        if not len(answerobj.answers):
            print "Not found."
        for ip in answerobj.answers:
            print "%s" % (ip['data']),
            url = "http://int.dpool.sina.com.cn/iplookup/iplookup.php?format%20=%20js&ip=" + ip['data']
            locall = urllib.urlopen(url).read()
            local = locall.decode("GBK");
            print '\t' + local[8:]
    except:
        print 'BAD DNS!'
'''

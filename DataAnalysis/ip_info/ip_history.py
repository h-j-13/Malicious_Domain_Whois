# coding=utf-8
import DNS
import sys
import MySQLdb
import time
import urllib2
import threading
import socket
import random


reload(sys)
sys.setdefaultencoding('utf-8')

lock0 = threading.Lock()
lock1 = threading.Lock()

dnslist = [['114.114.114.114'], ['114.114.115.115'], ['223.5.5.5'], ['223.6.6.6'], ['180.76.76.76'], ['1.2.4.8'],
           ['119.29.29.29'], ['182.254.116.116'], ['123.125.81.6'], ['140.207.198.6'], ['208.67.222.222'],
           ['208.67.220.220'], ['101.226.4.6']]

def wei(flag, digit, direct):
    #flag:source; digit:change which; direct:change digit to what
    front = 10 ** digit
    back = 10 ** (digit - 1)
    return int(flag/front)*front + direct*back + flag%back

def gen_ipstr(ip_set):
    ip_addr = ''
    for ip in ip_set:
        ip_addr = ip_addr + ip + ','
    if ip_addr == '':
        return ''
    else:
        return ip_addr[:-1]

def gethttpcode():
    conn = MySQLdb.connect(
        host='172.26.253.3',
        port=3306,
        user='root',
        passwd='platform'
    )
    conn.set_character_set('utf8')
    cur = conn.cursor()
    cur.execute("SET NAMES utf8")
    cur.execute("use malicious_domain_sys;")
    conn.commit()
    i = 0
    while 1 == 1:
        #ip_addr = ''
        ip_set = set()
        flag = 1
        domain = ''
        if lock0.acquire():
            try:  # 取出一个域名
                domain, ip_old, t_flag = result.pop()
                times = int(t_flag/1000) % 10
                if times == 0:
                    times = 9
                lock0.release()
            except:  # 域名池为空
                #print "return"
                lock0.release()
                cur.close()
                conn.commit()
                conn.close()
                return
        ip_old_set = set(ip_old.split(','))
        #n = hash(domain)%len(dnslist)
        DNS.defaults['server'] = '223.6.6.6'#dnslist[n]
        # print domain + "\t" + DNS.defaults['server'][0]
        reqobj = DNS.Request()
        try:
            answerobj = reqobj.req(name=domain, qtype=DNS.Type.A)
            if not len(answerobj.answers):
                flag = 2
        except:
            flag = 3
        if flag ==1:
            for ip in answerobj.answers:
                # print ip['data']
                ip_set.add(ip['data'])
            if times != 1:
                times -= 1
                if not ip_set.issubset(ip_old_set):
                    ip_set = ip_set | ip_old_set
                    ip_addr = gen_ipstr(ip_set)
                    t_flag = wei(wei(t_flag,3,flag),4,times)
                    cur.execute(
                        "UPDATE malicious_info SET IP = '%s', flag = %d, IP_detect_time= '%s' WHERE id = %d" % (
                        ip_addr, t_flag, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), hash(domain)))
                    #print domain + ' : ' + str(ip_old_set) + ' -> ' + str(ip_set) + '    <' + str(t_flag) + '>'
                    conn.commit()
                else:
                    t_flag = wei(wei(t_flag, 3, flag), 4, times)
                    cur.execute(
                        "UPDATE malicious_info SET flag = %d WHERE id = %d" % (
                            t_flag, hash(domain)))
                    conn.commit()
            else:
                print "==1"
                if not ip_set.issubset(ip_old_set):
                    ip_addr = gen_ipstr(ip_set)
                    t_flag = wei(wei(t_flag, 3, flag),4,9)
                    cur.execute("INSERT INTO ip_history1 (ID,IP,record_time) SELECT ID,SUBSTRING_INDEX(IP, ',', 1),IP_detect_time FROM malicious_info WHERE malicious_info.ID = %d" % hash(domain))
                    cur.execute(
                        "UPDATE malicious_info SET IP = '%s', flag = %d, IP_detect_time= '%s' WHERE id = %d" % (ip_addr, t_flag, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),  hash(domain)))
                    print domain+' : '+str(ip_old_set)+' -> '+str(ip_set) + '    <' + str(t_flag) + '>'
                    conn.commit()

        #flag==============


if __name__ == "__main__":
    # start = datetime.datetime.now()
    socket.setdefaulttimeout(10)
    conn = MySQLdb.connect(
        host='172.26.253.3',
        port=3306,
        user='root',
        passwd='platform'
    )
    conn.set_character_set('utf8')
    cur = conn.cursor()
    cur.execute("SET NAMES utf8")
    cur.execute("use malicious_domain_sys;")
    conn.commit()


    old_time = 0.0
    while True:
        new_time = time.time()
        if new_time-old_time<10800:
            time.sleep(100)
        else:
            threads = []
            print '##Run at '+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            old_time = new_time
            ncount = cur.execute(
                "SELECT domain_index.domain, malicious_info.IP, malicious_info.flag FROM malicious_info LEFT JOIN domain_index ON malicious_info.id = domain_index.id")
            print ncount
            result = list(cur.fetchall())
            #cur.close()
            #conn.close()
            i = 10
            while i > 0:
                th = threading.Thread(target=gethttpcode)
                threads.append(th)
                i -= 1
            for th in threads:
                th.setDaemon(True)
                th.start()
            for th in threads:
                th.join()
            print "##Finish"

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

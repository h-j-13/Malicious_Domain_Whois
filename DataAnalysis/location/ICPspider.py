#encoding:UTF-8
"""
功能：利用数据库中的domain信息，从网站上爬取icp信息(多线程)
作者:郑乐斌
更新时间:2016.8.10
"""

import re
import os
import time
import MySQLdb
import urllib
import urllib2
import threading
from threading import Thread
from Queue import Queue
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
num_thread = 10      # 线程数量
queue = Queue()     # 任务队列
domains = []    # 存储域名

# class BaseDb(object):

#     def __init__(self):
#         try:
#             self.db = MySQLdb.connect(host='172.26.253.3', 
#                             user='root', 
#                             passwd='platform',
#                             charset = "utf8",
#                             db='zgx')

#             self.cur = self.db.cursor()
#             # self.f = open('ICP_info.txt','a')
        
#         except Exception,e:
#             raise e

class Spider():


    def work(self):
        
        global success_num
        global fail_num
        success_num = 0
        fail_num = 0
        db = MySQLdb.connect(host='172.26.253.3',
                            user='root',
                            passwd='platform',
                            charset = "utf8",
                            db='malicious_domain_sys')
        db.set_character_set('utf8')
        cur = db.cursor()
        cur.execute("SET NAMES utf8")

        while 1:


            flag = queue.get()

            # queue中有1-100，根据数字设置起始和结束位置
            start = (flag - 1) * 200 + 1
            end = flag * 200

            for domain in domains[start:end]:
                
                url = "http://www.beianbeian.com/search/" + domain[1]
                while 1==1:#对于偶尔的网络故障，一直重试
                    try:
                        response = urllib2.urlopen(url)
                        # 创建Beautiful对象,传入网页内容(html格式)
                        soup = BeautifulSoup(response, "lxml")
                        # 遍历输出所有符合条件的标签
                        regular = '^/beianxinxi/'
                        address_info = soup.find_all(href = re.compile(regular))
                        # f = open('address_info3.txt','a')
                    except :
                        time.sleep(5)
                        continue

                    if len(address_info) != 0:

                        success_num += 1
                        # 保存域名备案信息
                        # f.write(str(success_num) + '.' + str(domain[0]) + '--' + str(address_info[0].string) + '\n')
                        print str(success_num) + '.' + str(domain[1]) + '--' + str(address_info[0].string)\
                        # print isinstance(s, unicode) # 用来判断是否为unicode
                        try:
                            ##f = open('ICP_info.txt','a')
                            ##f.write(str(success_num) + '--' + str(domain[0]) + '--' + str(address_info[0].string) + '\n')
                            # f = open('ICP_info.txt','a')

                            # 保存域名备案信息
                            # texts[domain[0]] = address_info[0].string
                            # self.f.write(str(success_num) + '**' + str(domain[0]) + '**' + str(address_info[0].string) + '\n')
                            # f.close()


                            # # 得到icp信息的域名在数据库中进行更新

                            sql = 'UPDATE locate SET ICP = "%s", ICP_province = "%s", flag=(flag div 10)*10+1 WHERE id = %d' % (address_info[0].string, self.get_province(address_info[0].string), hash(domain[1]))
                            count = cur.execute(sql)
                            db.commit()
                            time.sleep(1)  # 去掉偶尔会出现错误

                        except MySQLdb.Error,e:
                            raise e

                    else:
                        fail_num += 1
                        # f.write(str(domain[0]) + '--' + 'No icp information!' + '\n')

                        print str(fail_num) + '.' + str(domain[1]) + '--' + 'No icp information!'
                        try:
                            ##f = open('ICP_info.txt','a')
                            ##f.write(str(fail_num) + '--' + str(domain[0]) + '--' + 'No icp information!' + '\n')
                            # f = open('ICP_info.txt','a')

                            # 保存域名备案信息
                            # texts[domain[0]] = address_info[0].string
                            # self.f.write(str(success_num) + '**' + str(domain[0]) + '**' + str(address_info[0].string) + '\n')
                            # f.close()

                            # db = MySQLdb.connect(host='172.26.253.3',
                            #                 user='root',
                            #                 passwd='platform',
                            #                 charset = "utf8",
                            #                 db='zgx')

                            # cur = db.cursor()
                            # # 得到icp信息的域名在数据库中进行更新
                            sql = 'UPDATE locate SET ICP = "%s", ICP_province = "%s", flag=(flag div 10)*10+2 WHERE id = %d' % ( 'No results', '', hash(domain[1]))
                            count = cur.execute(sql)
                            db.commit()
                            time.sleep(1)  # 去掉偶尔会出现错误
                            # db.close()

                        except MySQLdb.Error,e:
                            print e
                            #raise e
                    break
            print 'Success:' + str(success_num) + ',' + 'Fail:' +  str(fail_num)
            queue.task_done()
            break
            

    def get_domains(self):

        global domains
        domains = []
        results = []
        try:
            db = MySQLdb.connect(host='172.26.253.3',
                            user='root', 
                            passwd='platform',
                            charset = "utf8",
                            db='malicious_domain_sys')

            cur = db.cursor()
            sql = 'SELECT locate.id, domain_index.domain FROM locate,domain_index WHERE locate.id = domain_index.id AND locate.flag > 0 AND locate.flag mod 10 = 0'
            count = cur.execute(sql)
            # results = cur.fetchall()
            domains = cur.fetchall()
            # for result in results:
            #     if result[0].split('.')[-1] == 'cn':
            #         domains.append(result[0])
            db.close()

        except MySQLdb.Error,e:
            raise e
            

    def create_queue(self):
        for i in xrange(1, 101):    # 创建任务队列，1-10
            queue.put(i)

    def creat_thread(self):
        for q in range(num_thread):    # 开始任务
            worker = Thread(target=self.work)
            worker.setDaemon(True)
            worker.start()
        queue.join()

    def get_province(self, icp):

        # address = ['京','津','冀','晋','蒙','辽','吉','黑','沪','苏','浙','皖',
        #            '闽','赣','鲁','豫','鄂','湘','粤','桂','琼','渝','川','贵',
        #            '云','藏','陕','甘','青','新','蜀','滇','陇','黔']

        address = {'京': '北京', '津': '天津', '冀': '河北', '晋': '山西', '蒙': '内蒙古', '辽': '辽宁', '吉': '吉林',
                   '黑': '黑龙江', '沪': '上海', '苏': '江苏', '浙': '浙江', '皖': '安徽', '黔': '贵州', '宁': '宁夏',
                   '闽': '福建', '赣': '江西', '鲁': '山东', '豫': '河南', '鄂': '湖北', '湘': '湖南', '粤': '广东',
                   '桂': '广西', '琼': '海南', '渝': '重庆', '川': '四川', '贵': '贵州', '滇': '云南', '陇': '甘肃',
                   '云': '云南', '藏': '西藏', '陕': '陕西', '甘': '甘肃', '青': '青海', '新': '新疆', '蜀': '四川',
                   '淅': '浙江', '卾': '湖北', '港': '香港'}
        for add in address.keys():
            if add in icp:
                return address[add]



if __name__ == '__main__':
 
    # 创建任务队列
    Spider().create_queue()
    # 从数据库中获取domain信息
    Spider().get_domains()
    # 创建线程
    Spider().creat_thread()
    

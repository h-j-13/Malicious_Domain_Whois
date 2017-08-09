# _*_ coding:utf-8 _*_
import urllib2
import urllib
import random
import time
# from threading import Timer
import re
import os
import MySQLdb
# from multiprocessing.dummy import Pool as ThreadPool
# import requests
import urlparse
# from lxml import  etree
# import schedule
# import threading
import socket

socket.setdefaulttimeout(2)
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import json

def outp(t):
    if t:
        for tt in t:
            print tt,
        print
    else:
        print None


class Phone(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host="172.26.253.3", user="root", passwd="platform", db="zgx",
                                    charset='utf8')
        self.cursor = self.conn.cursor()
        self.strlst=[]

    def __del__(self):
        self.conn.close()
        self.cursor.close()

    def analysis(self, phone1):  # 要更新的表的相关参数

        # 取出要匹配的国内区号，全部的数据源信息均在此库中，游标是self.cursor

        sql = "SELECT * FROM telphone \
        WHERE (id > '%d')" % (0)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()  # 区号
            if (phone1):
                flag = 0
                if ((phone1[0:5] == "+86.0") or (phone1[0:6] == "+086.0")):  # 属于中国大陆地区的标准格式的固定电话或者可能是一些不标准格式的手机号
                    country = "中国"
                    phone = phone1.split('.')[1]  # 取小数点右边的固定电话号段
                    for row in results:
                        quhao = row[1]
                        if quhao:
                            length = len(quhao)
                            phone_quhao = phone[0:length]

                            if (quhao == phone_quhao):
                                flag = 1
                                return country, row[2], row[3]
                                #print country + '\t' + row[2] + '\t' + row[3] + '\t' + phone1



                    if (flag == 0):  # ".0"却匹配不到相应的固定电话，可能是一些手机号段的不标准格式，去掉小数点后的“0”，获取之后的手机号7位
                        str_tel_deal = phone[1:8]  # 取手机号段的前7位,即小数点后的“0”不取
                        sql_2 = "SELECT * FROM phone_china2 WHERE phone = '%s'" % (
                        str_tel_deal)  # 根据索引直接去数据源表中相关地址查询省份和城市
                        self.cursor.execute(sql_2)
                        results_2 = self.cursor.fetchall()
                        if (results_2):
                            for row_2 in results_2:
                                #str_province = row_2[3]
                                #str_city = row_2[4]
                                #print "中国" + '\t' + row_2[3] + '\t' + row_2[4] + '\t' + phone1
                                #flag = 1
                                return "中国", row_2[3], row_2[4]


                elif (((phone1[0:4] == "+86.") and ((phone1[4] != "0") and (phone1[4] != "1"))) or (
                            (phone1[0:5] == "+086.") and ((phone1[5] != "0") and (phone1[5] != "1")))):
                    # 可能是非标准格式的固定电话，小数点后第一位少了“0”
                    phone = phone1.split('.')[1]  # 取小数点右边的固定电话号段
                    str22 = "0"
                    phone = str22 + phone
                    for row in results:
                        quhao = row[1]
                        if quhao:
                            length = len(quhao)
                            phone_quhao = phone[0:length]

                            if (quhao == phone_quhao):
                                flag = 1
                                #print "中国" + '\t' + row[2] + '\t' + row[3] + '\t' + phone1
                                return "中国", row[2], row[3]

                elif ((phone1[0:5] == "+86.1") or (phone1[0:6] == "+086.1")):  # 国内标准的手机号格式
                    country = "中国"
                    str222 = phone1.split('.')[1]  # 取小数点右边的手机号段
                    str_tel_deal = str222[0:7]  # 取手机号段的前7位
                    sql_2 = "SELECT * FROM phone_china2 WHERE phone = '%s'" % (str_tel_deal)  # 根据索引直接去数据源表中相关地址查询省份和城市
                    self.cursor.execute(sql_2)
                    results_2 = self.cursor.fetchall()
                    if (results_2):
                        flag = 1
                        for row_2 in results_2:
                            str_province = row_2[3]  # 为拼接字符串加上’‘
                            str_city = row_2[4]
                            #print "中国" + '\t' + row_2[3] + '\t' + row_2[4] + '\t' + phone1
                            return "中国", row_2[3], row_2[4]


                elif ((phone1[0:4] != "+86.") and (phone1[0:5] != "+086.")):  # 国外的号段
                    pho = phone1.split('.')[0]  # 取小数点左边的表示国际区号的号段
                    str = "00"
                    phone_na_pre = str + pho[1:]

                    sql2 = "SELECT * FROM national WHERE quhao = '%s'" % (phone_na_pre)  # 根据索引直接去数据源表中相关国家
                    self.cursor.execute(sql2)
                    results2 = self.cursor.fetchall()
                    if (results2):
                        flag = 1
                        for row2 in results2:
                            str_country = row2[1]  # 找到的国家信息
                            #print phone1 + '\t' + str_country
                            return str_country,None,None



                    else:  # 一些固定电话的不标准格式，把省市区号写在应该写国家区号的地方，如：+021.33114562
                        phone_1 = phone1.split('.')[1]  # 取小数点右边的固定电话号段
                        phone_2 = phone1.split('.')[0]
                        phone = phone_2[1:] + phone_1
                        for row in results:
                            quhao = row[1]
                            if quhao:
                                length = len(quhao)
                                phone_quhao = phone[0:length]

                                if (quhao == phone_quhao):
                                    flag = 1
                                    #print row[2] + '\t' + row[3] + '\t' + phone1
                                    return "中国",row[2], row[3]
                                    country = "中国"

                        if (flag == 0):  # 可能是固定电话的非标准格式，即号段前少了“0”
                            str22 = "0"
                            phone = str22 + phone
                            for row in results:
                                quhao = row[1]
                                if quhao:
                                    length = len(quhao)
                                    phone_quhao = phone[0:length]

                                    if (quhao == phone_quhao):
                                        flag = 1
                                        #print row[2] + '\t' + row[3] + '\t' + phone1
                                        return "中国", row[2], row[3]
                                        country = "中国"


            return None,None,None
        except:
            #print "error 2222"
            return None,None,None


if __name__ == "__main__":
    p = Phone()

    outp(p.analysis("+021.33114562"))

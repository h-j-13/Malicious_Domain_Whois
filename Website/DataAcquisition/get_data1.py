# -*- coding: utf8 -*-

# 目的：信安大赛whois获取数据
# @author：周桐
# time:2017年4月9日

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from tools import *
import pymysql
import random
import datetime
import arrow
import json
import time

database.connect()

conn =pymysql.connect(host='172.26.253.3', user='root', passwd='platform', db='malicious_domain_sys', charset='utf8')
cur = conn.cursor()


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

#  获取恶意域名数量
def get_malicious_domain():
    malicious_domain = domain_index.select().where(domain_index.judge_flag < 0).count()
    return json.dumps(malicious_domain)

# 1.1恶意注册人注册域名情况
def get_black_name(cutoff):
    black_name = dict(info=[], dnsnum=0)
    sen = cur.execute(
        "SELECT r.info,r.malicious_count,r.domain_count FROM reg_info_black_lists AS r WHERE r.type=2 LIMIT %s,10",
        (cutoff - 1) * 10)
    name_data = cur.fetchall()
    black_name['dnsnum'] = reg_info_black_lists.select().where(reg_info_black_lists.type == 2).count()
    for data in name_data:

        black_name['info'].append({'name': data.info, 'Alldomain': data.domain_count, 'baddomain': data.malicious_count})

    return json.dumps(black_name, ensure_ascii=False)

# 1.2恶意电话注册域名情况
def get_black_tel(cutoff):
    black_tel = dict(info=[])
    sen = cur.execute(
        "SELECT r.info,r.malicious_count,r.domain_count FROM reg_info_black_lists AS r WHERE r.type=4 LIMIT %s,10",
        (cutoff - 1) * 10)
    tel_data = cur.fetchall()
    black_tel['dnsnum'] = reg_info_black_lists.select().where(reg_info_black_lists.type == 4).count()
    for data in tel_data:
        black_tel['info'].append({'name': data.info, 'Alldomain': data.domain_count, 'baddomain': data.malicious_count})

    return json.dumps(black_tel, ensure_ascii=False)

# 1.3恶意邮箱注册域名情况
def get_black_email(cutoff):
    black_email = dict(info=[])
    sen = cur.execute(
        "SELECT r.info,r.malicious_count,r.domain_count FROM reg_info_black_lists AS r WHERE r.type=3 LIMIT %s,10", (cutoff-1)*10)
    email_data = cur.fetchall()
    black_email['dnsnum'] = reg_info_black_lists.select().where(reg_info_black_lists.type == 3).count()
    for data in email_data:
        black_email['info'].append({'name': data[0], 'Alldomain': data[3], 'baddomain': data[2]})

    return json.dumps(black_email, ensure_ascii=False)

# 2.1所有恶意域名的whois信息展示   ￥￥￥
def get_malicious_domain_whois(k):

    malicious_domain_whois=dict(whoisall=[],whoisnum=0)
    sen = cur.execute(
        "SELECT * FROM whois AS w INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON w.ID=i.ID LIMIT %s,10",(k-1)*10)
    MDW_data = cur.fetchall()

    status_mapping = {"1": "ADDPERIOD", "2": "AUTORENEWPERIOD", "3": "INACTIVE", "4": "OK", "5": "PENDINGCREATE", "6": "PENDINGDELETE",
                      "7": "PENDINGRENEW", "8": "PENDINGRESTORE", "9": "PENDINGTRANSFER", "10": "PENDINGUPDATE", "11": "REDEMPTIONPERIOD",
                      "12": "RENEWPERIOD", "13": "SERVERDELETEPROHIBITED", "14": "SERVERHOLD", "15": "SERVERRENEWPROHIBITED",
                      "16": "SERVERTRANSFERPROHIBITED", "17": "SERVERUPDATEPROHIBITED", "18": "TRANSFERPERIOD", "19": "CLIENTDELETEPROHIBITED",
                      "20": "CLIENTHOLD", "21": "CLIENTRENEWPROHIBITED", "22": "CLIENTTRANSFERPROHIBITED", "23": "CLIENTUPDATEPROHIBITED",
                      "24": "ACTIVE", "25": "REGISTRYLOCK", "26": "REGISTRARLOCK", "27": "REGISTRYHOLD", "28": "REGISTRARHOLD", "29"
                      : "NOTEXIST", "30": "NOSTATUS ", "31": "CONNECT"}

    for data in MDW_data:
        status = ""
        for index in data[4].split(";"):
            if index in status_mapping.keys():
                status = status + status_mapping[index] + ";"
            else:
                status = status + index + ";"
        status = status[:-1]
        malicious_domain_whois['whoisall'].append(dict(domain=data[2], tld=data[3], condition=status, business=data[5],
                Firm=data[11], first=data[6], second=data[7], origin=data[16], name=data[8], tel=data[9],email=data[10],
                signin=data[13], duetime=data[14], update=data[15], servers=data[12], inserttime=data[17]))
    
    sen = cur.execute(
        "SELECT count(*) FROM whois AS w INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON w.ID=i.ID")
    num_data = cur.fetchone()
    malicious_domain_whois['whoisnum'] = num_data[0]
    return json.dumps(malicious_domain_whois, cls=DateEncoder, ensure_ascii=False)

# 2.2恶意域名注册商分布情况,topN(暂取10)
def get_malicious_sponsoring_registrar():
    sen = cur.execute("SELECT w.sponsoring_registrar,count(w.sponsoring_registrar) AS 'num' FROM whois AS w INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON w.ID=i.ID GROUP BY w.sponsoring_registrar ORDER BY num desc")
    MSR_data = cur.fetchall()
    sen1 = cur.execute("SELECT count(*) FROM whois AS w INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON w.ID=i.ID ")
    SR_sum = cur.fetchone()
    SR_sum = SR_sum[0]
    malicious_sponsoring_registrar = dict(info=[])
    try:
        for i in range(0, 10):
            SR_sum = SR_sum-MSR_data[i][1]
            if MSR_data[i][0] == '':
                malicious_sponsoring_registrar['info'].append({'registrar': '未知注册商', 'num': MSR_data[i][1]})
            else:
                malicious_sponsoring_registrar['info'].append({'registrar': MSR_data[i][0], 'num': MSR_data[i][1]})
        malicious_sponsoring_registrar['info'].append({'registrar': '其他注册商', 'num': SR_sum})
    except:
        pass
    return json.dumps(malicious_sponsoring_registrar, ensure_ascii=False)

# 2.3恶意域名的顶级域(TLD)分布 ￥￥￥
def get_malicious_tld():
    sen = cur.execute(
        "SELECT w.tld,count(w.tld) AS 'num' FROM whois AS w INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON w.ID=i.ID GROUP BY w.tld ORDER BY num desc")
    MSR_data = cur.fetchall()
    sen1 = cur.execute(
        "SELECT count(*) FROM whois AS w INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON w.ID=i.ID ")
    SR_sum = cur.fetchone()
    SR_sum = SR_sum[0]
    malicious_tld = dict(info=[])
    try:
        for i in range(0, 9):
            SR_sum = SR_sum - MSR_data[i][1]
            if MSR_data[i][0] == '':
                malicious_tld['info'].append({'tld': '未知tld', 'num': MSR_data[i][1]})
            else:
                malicious_tld['info'].append({'tld': MSR_data[i][0], 'num': MSR_data[i][1]})
        malicious_tld['info'].append({'tld':'其他tld', 'num':SR_sum})
    except:
        pass

    return json.dumps(malicious_tld, ensure_ascii=False)

# 3得到不同地域域名数量  ￥￥￥
def get_region_domain(mode):
    region_domain = {'天津':0, '上海':0, '重庆':0, '北京':0, '河北':0, '河南':0, '云南':0, '辽宁':0,
                         '黑龙江':0, '湖南':0, '安徽':0, '山东':0, '新疆':0, '江苏':0, '浙江':0, '江西':0, '湖北':0, '广西':0, '甘肃':0,
                         '山西':0, '内蒙古':0, '陕西':0, '吉林':0, '福建':0, '贵州':0, '广东':0, '青海':0, '西藏':0, '四川':0, '宁夏':0,
                         '海南':0, '台湾':0, '香港':0, '澳门':0}
    region_situation = dict(info=[], foreign=0, unknow=0)
    if mode == 1:#reg_whois_province来源
        sen = cur.execute(
            "SELECT l.reg_whois_province,count(l.reg_whois_province) AS 'num' FROM locate AS l INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON l.ID=i.ID WHERE l.reg_whois_province!='' AND (UPPER(l.country)=UPPER('CN') OR UPPER(l.country)=UPPER('china')) GROUP BY l.reg_whois_province")
        RD_data = cur.fetchall()
        for data in RD_data:
            region_domain[data[0]] = data[1]

        for key in region_domain.keys():
            region_situation['info'].append({'name': key, 'value': region_domain[key]})

        sen1 = cur.execute(
            "SELECT count(*)  FROM locate AS l INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON l.ID=i.ID WHERE l.reg_whois_province=''")
        cant_resolve = cur.fetchone()
        region_situation['unknow'] = cant_resolve[0]

        sen2 = cur.execute(
            "SELECT count(*) FROM locate AS l INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON l.ID=i.ID WHERE l.country!='' AND UPPER(l.country)!=UPPER('CN') AND UPPER(l.country)!=UPPER('china')")
        foreign_domain = cur.fetchone()
        region_situation['foreign'] = foreign_domain[0]
        return json.dumps(region_situation, ensure_ascii=False)

    elif mode == 2:  # reg_postal_province来源
        sen = cur.execute(
            "SELECT l.reg_postal_province,count(l.reg_postal_province) AS 'num' FROM locate AS l INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON l.ID=i.ID WHERE l.reg_postal_province!='' AND (UPPER(l.country)=UPPER('CN') OR UPPER(l.country)=UPPER('china')) GROUP BY l.reg_postal_province")
        RD_data = cur.fetchall()
        for data in RD_data:
            region_domain[data[0]] = data[1]

        for key in region_domain.keys():
            region_situation['info'].append({'name': key, 'value': region_domain[key]})

        sen1 = cur.execute(
            "SELECT count(*) FROM locate AS l INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON l.ID=i.ID WHERE l.reg_postal_province=''")
        cant_resolve = cur.fetchone()
        region_situation['unknow'] = cant_resolve[0]

        sen2 = cur.execute(
            "SELECT count(*) FROM locate AS l INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON l.ID=i.ID WHERE l.country!='' AND UPPER(l.country)!=UPPER('CN') AND UPPER(l.country)!=UPPER('china')")
        foreign_domain = cur.fetchone()
        region_situation['foreign'] = foreign_domain[0]
        return json.dumps(region_situation, ensure_ascii=False)

    elif mode == 3:  # reg_phone_province来源
        sen = cur.execute(
            "SELECT l.reg_phone_province,count(l.reg_phone_province) AS 'num' FROM locate AS l INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON l.ID=i.ID WHERE l.reg_phone_province!='' AND (UPPER(l.country)=UPPER('CN') OR UPPER(l.country)=UPPER('china')) GROUP BY l.reg_phone_province")
        RD_data = cur.fetchall()
        for data in RD_data:
            region_domain[data[0]] = data[1]

        for key in region_domain.keys():
            region_situation['info'].append({'name': key, 'value': region_domain[key]})

        sen1 = cur.execute(
            "SELECT count(*) FROM locate AS l INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON l.ID=i.ID WHERE l.reg_phone_province=''")
        cant_resolve = cur.fetchone()
        region_situation['unknow'] = cant_resolve[0]

        sen2 = cur.execute(
            "SELECT count(*) FROM locate AS l INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON l.ID=i.ID WHERE l.country!='' AND UPPER(l.country)!=UPPER('CN') AND UPPER(l.country)!=UPPER('china')")
        foreign_domain = cur.fetchone()
        region_situation['foreign'] = foreign_domain[0]
        return json.dumps(region_situation, ensure_ascii=False)

    elif mode == 4:  # IP_info来源
        sen = cur.execute(
            "SELECT l.IP_info FROM locate AS l INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON l.ID=i.ID WHERE l.IP_info!='' AND (UPPER(l.country)=UPPER('CN') OR UPPER(l.country)=UPPER('china'))")
        RD_data = cur.fetchall()
        for data in RD_data:

            if data[0].split('省')[0].split('|')[-1] in region_domain.keys():
                region_domain[str(data[0].split('省')[0].split('|')[-1])] += 1
            elif data[0].split('|')[0].split(',')[-1] in region_domain.keys():
                region_domain[str(data[0].split('|')[0].split(',')[-1])] += 1
            elif data[0].split('|')[0].split(',')[-1] not in region_domain.keys() and data[0].split('|')[0].split(',')[-1] != '中国':
                region_situation['foreign'] = 1 + region_situation['foreign']

        for key in region_domain.keys():
            region_situation['info'].append({'name': key, 'value': region_domain[key]})

        sen1 = cur.execute(
            "SELECT count(*) FROM locate AS l INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON l.ID=i.ID WHERE l.IP_info=''")
        cant_resolve = cur.fetchone()
        region_situation['unknow'] = cant_resolve[0]

        sen2 = cur.execute(
            "SELECT count(*) FROM locate AS l INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON l.ID=i.ID WHERE l.country!='' AND UPPER(l.country)!=UPPER('CN') AND UPPER(l.country)!=UPPER('china')")
        foreign_domain = cur.fetchone()
        region_situation['foreign'] = foreign_domain[0] + region_situation['foreign']
        return json.dumps(region_situation, ensure_ascii=False)

    elif mode == 5:  # ICP_province来源
        sen = cur.execute(
            "SELECT l.ICP_province,count(l.ICP_province) AS 'num' FROM locate AS l INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON l.ID=i.ID WHERE l.ICP_province!='' AND (UPPER(l.country)=UPPER('CN') OR UPPER(l.country)=UPPER('china')) GROUP BY l.ICP_province")
        RD_data = cur.fetchall()
        for data in RD_data:
            region_domain[data[0]] = data[1]

        for key in region_domain.keys():
            region_situation['info'].append({'name': key, 'value': region_domain[key]})

        sen1 = cur.execute(
            "SELECT count(*) FROM locate AS l INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON l.ID=i.ID WHERE l.ICP_province=''")
        cant_resolve = cur.fetchone()
        region_situation['unknow'] = cant_resolve[0]

        sen2 = cur.execute(
            "SELECT count(*) FROM locate AS l INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON l.ID=i.ID WHERE l.country!='' AND UPPER(l.country)!=UPPER('CN') AND UPPER(l.country)!=UPPER('china')")
        foreign_domain = cur.fetchone()
        region_situation['foreign'] = foreign_domain[0]
        return json.dumps(region_situation, ensure_ascii=False)

    else:
        pass

# 4.1某年创建/到期数量展示
def get_c_e_data(chooseyear):

    date_data = dict(year=[{"name":"一月", "cValue":0, "eValue":0}, {"name":"二月", "cValue":0, "eValue":0}, {"name":"三月", "cValue":0, "eValue":0}, {"name":"四月", "cValue":0, "eValue":0}, {"name":"五月", "cValue":0, "eValue":0}, {"name":"六月", "cValue":0, "eValue":0}, {"name":"七月", "cValue":0, "eValue":0}, {"name":"八月", "cValue":0, "eValue":0}, {"name":"九月", "cValue":0, "eValue":0}, {"name":"十月", "cValue":0, "eValue":0}, {"name":"十一月", "cValue":0, "eValue":0}, {"name":"十二月", "cValue":0, "eValue":0}], c_date=[], e_date=[])

    standard_year = 2003
    for year in range(standard_year, chooseyear+1):
        date_data['c_date'].append({"name": year,"value":0})
        date_data['e_date'].append({"name": year, "value": 0})

    data = whois.select(whois.creation_date).where(whois.creation_date != '')
    for date in data:
        try:
            try:
                time = arrow.get(date.creation_date, 'DD-MMM-YYYY')
                date_data['c_date'][time.year-standard_year]['value'] += 1
                if time.year == chooseyear:
                    date_data['year'][time.month-1]["cValue"] += 1

            except:
                time = arrow.get(date.creation_date)
                date_data['c_date'][time.year - standard_year]['value'] += 1
                if time.year == chooseyear:
                    date_data['year'][time.month - 1]["cValue"] += 1

        except:
            pass

    data1 = whois.select(whois.expiration_date).where(whois.expiration_date != '')

    for date in data1:
        try:
            try:
                time = arrow.get(date.expiration_date, 'DD-MMM-YYYY')
                date_data['e_date'][time.year - standard_year]['value'] += 1
                if time.year == chooseyear:
                    date_data['year'][time.month - 1]["eValue"] += 1

            except:
                time = arrow.get(date.expiration_date)
                date_data['e_date'][time.year - standard_year]['value'] += 1
                if time.year == chooseyear:
                    date_data['year'][time.month - 1]["eValue"] += 1

        except:
            pass

    return json.dumps(date_data, ensure_ascii=False)

# 4.2恶意域名总体生存时间分布展示   横轴动态定
def get_exist_situation():
    exist_situation = dict(info=[])
    sen = cur.execute(
        "SELECT w.creation_date FROM whois AS w INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON w.ID=i.ID AND w.creation_date != ''")
    exist_data = cur.fetchall()
    timenow = arrow.now()

    days_data = []
    for data in exist_data:
        try:
            try:
                time = arrow.get(data[0], 'DD-MMM-YYYY')
                days_data.append((timenow - time).days)
            except:
                time = arrow.get(data[0])
                days_data.append((timenow - time).days)
        except:
            pass

    # 数据处理，排序后通过比较数后数的索引计数
    try:
        days_data = sorted(days_data)
        base = int((days_data[-1] - days_data[0])/15)
        lastnum = -1
        multiple = 1
        for i in range(0, len(days_data)-1):
            if (base*multiple+days_data[0] >= days_data[i]) and (base*multiple+days_data[0] < days_data[i+1]):
                exist_situation['info'].append({'x': str(base*(multiple-1)), 'y': i-lastnum})
                multiple += 1
                lastnum = i
            if multiple == 15:
                break
        exist_situation['info'].append({'x': str(base * (multiple-1)), 'y': len(days_data) - lastnum})
    except:
        pass
    return json.dumps(exist_situation, ensure_ascii=False)

# 4.3恶意域名最近更新时间分布
def get_update_situation():
    update_situation = dict(info=[])
    sen = cur.execute(
        "SELECT w.updated_date FROM whois AS w INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON w.ID=i.ID AND w.updated_date != ''")
    updated_data = cur.fetchall()
    timenow = arrow.now()

    try:
        minutes_data = []
        for data in updated_data:
            try:
                try:
                    time = arrow.get(data[0], 'DD-MMM-YYYY')
                    minutes_data.append((timenow - time).days)
                except:
                    time = arrow.get(data[0])
                    minutes_data.append((timenow - time).days)
            except:
                pass

        # 数据处理，取前百分之九十五进行统计最近时间
        minutes_data = sorted(minutes_data)[0:int(95*len(minutes_data)/100)]
        base = int((minutes_data[-1] - minutes_data[0])/15)
        lastnum = -1
        multiple = 1
        for i in range(0, len(minutes_data)-1):
            if (base*multiple+minutes_data[0] >= minutes_data[i]) and (base*multiple+minutes_data[0] < minutes_data[i+1]):
                update_situation['info'].append({'x': str(base*(multiple-1)), 'y': i-lastnum})
                multiple += 1
                lastnum = i
            if multiple == 15:
                break
        update_situation['info'].append({'x': str(base * (multiple-1)), 'y': len(minutes_data) - lastnum})
    except:
        pass

    return json.dumps(update_situation,ensure_ascii=False)

# 5.1总体恶意域名解析情况  available对应情况需要确定（暂定-10可以，1不可以）￥￥￥
def get_bad_domain_situation():
    bad_domain_situation = dict()
    sen =  cur.execute("SELECT count(*) FROM malicious_info AS m INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON m.ID=i.ID WHERE m.available=1")
    bad_domain_situation['Online'] = cur.fetchone()[0]
    sen = cur.execute(
        "SELECT count(*) FROM malicious_info AS m INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON m.ID=i.ID WHERE m.available!=1")
    bad_domain_situation['Offline'] = cur.fetchone()[0]

    return json.dumps(bad_domain_situation)

# 5.2总体恶意域名IP更换频率 暂定分八组
def get_ip_frequency():
    sen = cur.execute(
        "SELECT l.ID,l.record_time FROM ip_history AS l INNER JOIN (SELECT d.ID FROM domain_index AS d WHERE d.judge_flag<0) AS i ON l.ID=i.ID ORDER BY l.ID,l.record_time desc")
    IF_data = cur.fetchall()

    time_data = []
    temp_time = 0
    id = 0
    for data in IF_data:
        if temp_time == 0:
            temp_time = data[1]
            id = data[0]
        elif data[0] != id:
            id = data[0]
            temp_time = data[1]
        else:
            time_data.append((temp_time - data[1]).days)
            id = data[0]
            temp_time = data[1]
    ip_frequency = dict(info=[])
    try:
        MIN = min(time_data)
        MAX = max(time_data)
        index = int((MAX - MIN)/15)

        for i in range(0, 15):
            ip_frequency['info'].append({'x': index*i, 'y': 0})

        for fre in time_data:
            key = int((fre-MIN)/index) if fre == MAX else int((fre-MIN)/index)+1
            ip_frequency['info'][key-1]['y'] = 1+ip_frequency['info'][key-1]['y']
    except:
        pass

    return ip_frequency

# 第二模块

# 获取查询信息
def get_check_info(uuid):
    check_info = dict(base_info=dict(), same_event=[dict()], show_img=dict(seen="false"),
                    ip=[], analysis=[{}], node=[], whois=[], position=[], geoCoordMap=dict(), state=0, edges=[])

    #  whois
    BI_data_whois = whois.select(whois.domain, whois.tld, whois.domain_status, whois.sponsoring_registrar, whois.
                                 top_whois_server, whois.sec_whois_server, whois.reg_name, whois.reg_phone,
                                 whois.reg_email,
                                 whois.org_name,
                                 whois.name_server, whois.creation_date, whois.expiration_date, whois.updated_date,
                                 whois.details,
                                 whois.insert_time).where(whois.ID == uuid)

    for data in BI_data_whois:
        status_mapping = {"1": "ADDPERIOD", "2": "AUTORENEWPERIOD", "3": "INACTIVE", "4": "OK", "5": "PENDINGCREATE",
                          "6": "PENDINGDELETE",
                          "7": "PENDINGRENEW", "8": "PENDINGRESTORE", "9": "PENDINGTRANSFER", "10": "PENDINGUPDATE",
                          "11": "REDEMPTIONPERIOD",
                          "12": "RENEWPERIOD", "13": "SERVERDELETEPROHIBITED", "14": "SERVERHOLD",
                          "15": "SERVERRENEWPROHIBITED",
                          "16": "SERVERTRANSFERPROHIBITED", "17": "SERVERUPDATEPROHIBITED", "18": "TRANSFERPERIOD",
                          "19": "CLIENTDELETEPROHIBITED",
                          "20": "CLIENTHOLD", "21": "CLIENTRENEWPROHIBITED", "22": "CLIENTTRANSFERPROHIBITED",
                          "23": "CLIENTUPDATEPROHIBITED",
                          "24": "ACTIVE", "25": "REGISTRYLOCK", "26": "REGISTRARLOCK", "27": "REGISTRYHOLD",
                          "28": "REGISTRARHOLD", "29"
                          : "NOTEXIST", "30": "NOSTATUS ", "31": "CONNECT"}

        status = ""
        for index in data.domain_status.split(";"):
            if index in status_mapping.keys():
                status = status + status_mapping[index] + ";"
            else:
                status = status + index + ";"
        status = status[:-1]

        check_info['whois'] = [{
            "name": "域名",
            "info": data.domain
        }, {
            "name": "tld(AJAX)",
            "info": data.tld
        },{
            "name": "域名状态",
            "info": status
        },{
            "name": "一级whois服务器",
            "info": data.top_whois_server
        },{
            "name": "二级whois服务器",
            "info": data.sec_whois_server
        },{
            "name": "名称服务器",
            "info": data.name_server
        },{
            "name": "注册商",
            "info": data.sponsoring_registrar
        },{
            "name": "注册姓名",
            "info": data.reg_name
        },{
            "name": "注册者电话",
            "info": data.reg_phone
        },
        {
            "name": "注册者邮箱",
            "info": data.reg_email
        }, {
            "name": "注册公司",
            "info": data.org_name
        }, {
            "name": "whois记录创建时间",
            "info": data.creation_date
        }, {
            "name": "whois记录到期时间",
            "info": data.expiration_date
        }, {
            "name": "whois记录更新时间",
            "info": data.updated_date
        }, {
            "name": "原始whois记录",
            "info": data.details
        }, {
            "name": "信息插入时间",
            "info": data.insert_time
        }]


    #  ip
    BI_data_ip = ip_history.select(ip_history.IP).where(ip_history.ID == uuid).order_by('ip_history.record_time',
                                                                                 'desc')
    judge = 0
    for data in BI_data_ip:
        if judge == 0:
            check_info['ip'].append({"ipname": "当前ip", "ipinfo": data.IP})
        else:
            check_info['ip'].append({"ipname": "历史ip"+str(judge), "ipinfo": data.IP})
        judge += 1

    #  show_img
    PI_data = malicious_info.select(malicious_info.available, malicious_info.key_word, malicious_info.title,malicious_info.malicious_keywords).where(
        malicious_info.ID == uuid)
    keyword = ""
    check_info['show_img']['seen'] = "false"
    for data in PI_data:
        if data.available != 1:
            check_info['show_img']['seen'] = "false"

        else:
            check_info['show_img']['seen'] = "true"
            check_info['show_img']['dnstitle'] = data.title
            check_info['show_img']['dnskey'] = data.key_word
            check_info['show_img']['img'] = "http://cdn.jiemodui.com/img/Public/Uploads/item/20160318/1458282526729821.png"
            keyword = data.malicious_keywords

    # node,edges,state
    color = ['#4F4F4F', '#EA0000', '#D9006C', '#D200D2', '#8600FF', '#4A4AFF', '#00FFFF', '#8CEA00', '3FF5809',
             '#FFD306']
    related_info = dict(state=0, node=[], edges=[])

    RI_data = whois.select(whois.reg_name, whois.reg_phone, whois.reg_email).where(whois.ID == uuid)
    name, phone, email = '', '', ''
    for data in RI_data:
        name, phone, email = data.reg_name, data.reg_phone, data.reg_email
        related_info['state'] = 1
    if name == '':
        name = '1q2w3e4r'
    else:
        related_info['node'].append(
            {"color": "#ea0000", "label": name, "y": -500, "x": -250, "id": name, "size": 30})
    if phone == '':
        phone = '1q2w3e4r'
    else:
        related_info['node'].append(
            {"color": "#8cea00", "label": phone, "y": 0, "x": 0, "id": phone, "size": 30})
    if email == '':
        email = '1q2w3e4r'
    else:
        related_info['node'].append(
            {"color": "#4a4aff", "label": email, "y": 0, "x": -500, "id": email, "size": 30})

    all_point_data = whois.select(whois.domain).where(
        (whois.reg_name == name) | (whois.reg_email == email) | (whois.reg_phone == phone))
    for data in all_point_data:
        related_info['node'].append(
            {"color": random.choice(color), "label": data.domain, "y": random.uniform(-450, -50),
             "x": random.uniform(-450, -50), "id": data.domain, "size": 10})

    name_data = whois.select(whois.domain).where(
        (whois.reg_name == name) & (whois.reg_email != email) & (whois.reg_phone != phone))
    for data in name_data:
        related_info['edges'].append({"sourceID": name, "attributes": {}, "targetID": data.domain, "size": 1})

    email_data = whois.select(whois.domain).where(
        (whois.reg_name != name) & (whois.reg_email == email) & (whois.reg_phone != phone))
    for data in email_data:
        related_info['edges'].append({"sourceID": email, "attributes": {}, "targetID": data.domain, "size": 1})

    phone_data = whois.select(whois.domain).where(
        (whois.reg_name != name) & (whois.reg_email != email) & (whois.reg_phone == phone))
    for data in phone_data:
        related_info['edges'].append({"sourceID": phone, "attributes": {}, "targetID": data.domain, "size": 1})

    check_info['node'] = related_info['node']
    check_info['state'] = related_info['state']
    check_info['edges'] = related_info['edges']

    # position
    city_coordinate = {'海门': [121.15, 31.89],
                       '鄂尔多斯': [109.781327, 39.608266],
                       '招远': [120.38, 37.35],
                       '舟山': [122.207216, 29.985295],
                       '齐齐哈尔': [123.97, 47.33],
                       '盐城': [120.13, 33.38],
                       '赤峰': [118.87, 42.28],
                       '青岛': [120.33, 36.07],
                       '乳山': [121.52, 36.89],
                       '金昌': [102.188043, 38.520089],
                       '泉州': [118.58, 24.93],
                       '莱西': [120.53, 36.86],
                       '日照': [119.46, 35.42],
                       '胶南': [119.97, 35.88],
                       '南通': [121.05, 32.08],
                       '拉萨': [91.11, 29.97],
                       '云浮': [112.02, 22.93],
                       '梅州': [116.1, 24.55],
                       '文登': [122.05, 37.2],
                       '上海': [121.48, 31.22],
                       '攀枝花': [101.718637, 26.582347],
                       '威海': [122.1, 37.5],
                       '承德': [117.93, 40.97],
                       '厦门': [118.1, 24.46],
                       '汕尾': [115.375279, 22.786211],
                       '潮州': [116.63, 23.68],
                       '丹东': [124.37, 40.13],
                       '太仓': [121.1, 31.45],
                       '曲靖': [103.79, 25.51],
                       '烟台': [121.39, 37.52],
                       '福州': [119.3, 26.08],
                       '瓦房店': [121.979603, 39.627114],
                       '即墨': [120.45, 36.38],
                       '抚顺': [123.97, 41.97],
                       '玉溪': [102.52, 24.35],
                       '张家口': [114.87, 40.82],
                       '阳泉': [113.57, 37.85],
                       '莱州': [119.942327, 37.177017],
                       '湖州': [120.1, 30.86],
                       '汕头': [116.69, 23.39],
                       '昆山': [120.95, 31.39],
                       '宁波': [121.56, 29.86],
                       '湛江': [110.359377, 21.270708],
                       '揭阳': [116.35, 23.55],
                       '荣成': [122.41, 37.16],
                       '连云港': [119.16, 34.59],
                       '葫芦岛': [120.836932, 40.711052],
                       '常熟': [120.74, 31.64],
                       '东莞': [113.75, 23.04],
                       '河源': [114.68, 23.73],
                       '淮安': [119.15, 33.5],
                       '泰州': [119.9, 32.49],
                       '南宁': [108.33, 22.84],
                       '营口': [122.18, 40.65],
                       '惠州': [114.4, 23.09],
                       '江阴': [120.26, 31.91],
                       '蓬莱': [120.75, 37.8],
                       '韶关': [113.62, 24.84],
                       '嘉峪关': [98.289152, 39.77313],
                       '广州': [113.23, 23.16],
                       '延安': [109.47, 36.6],
                       '太原': [112.53, 37.87],
                       '清远': [113.01, 23.7],
                       '中山': [113.38, 22.52],
                       '昆明': [102.73, 25.04],
                       '寿光': [118.73, 36.86],
                       '盘锦': [122.070714, 41.119997],
                       '长治': [113.08, 36.18],
                       '深圳': [114.07, 22.62],
                       '珠海': [113.52, 22.3],
                       '宿迁': [118.3, 33.96],
                       '咸阳': [108.72, 34.36],
                       '铜川': [109.11, 35.09],
                       '平度': [119.97, 36.77],
                       '佛山': [113.11, 23.05],
                       '海口': [110.35, 20.02],
                       '江门': [113.06, 22.61],
                       '章丘': [117.53, 36.72],
                       '肇庆': [112.44, 23.05],
                       '大连': [121.62, 38.92],
                       '临汾': [111.5, 36.08],
                       '吴江': [120.63, 31.16],
                       '石嘴山': [106.39, 39.04],
                       '沈阳': [123.38, 41.8],
                       '苏州': [120.62, 31.32],
                       '茂名': [110.88, 21.68],
                       '嘉兴': [120.76, 30.77],
                       '长春': [125.35, 43.88],
                       '胶州': [120.03336, 36.264622],
                       '银川': [106.27, 38.47],
                       '张家港': [120.555821, 31.875428],
                       '三门峡': [111.19, 34.76],
                       '锦州': [121.15, 41.13],
                       '南昌': [115.89, 28.68],
                       '柳州': [109.4, 24.33],
                       '三亚': [109.511909, 18.252847],
                       '自贡': [104.778442, 29.33903],
                       '吉林': [126.57, 43.87],
                       '阳江': [111.95, 21.85],
                       '泸州': [105.39, 28.91],
                       '西宁': [101.74, 36.56],
                       '宜宾': [104.56, 29.77],
                       '呼和浩特': [111.65, 40.82],
                       '成都': [104.06, 30.67],
                       '大同': [113.3, 40.12],
                       '镇江': [119.44, 32.2],
                       '桂林': [110.28, 25.29],
                       '张家界': [110.479191, 29.117096],
                       '宜兴': [119.82, 31.36],
                       '北海': [109.12, 21.49],
                       '西安': [108.95, 34.27],
                       '金坛': [119.56, 31.74],
                       '东营': [118.49, 37.46],
                       '牡丹江': [129.58, 44.6],
                       '遵义': [106.9, 27.7],
                       '绍兴': [120.58, 30.01],
                       '扬州': [119.42, 32.39],
                       '常州': [119.95, 31.79],
                       '潍坊': [119.1, 36.62],
                       '重庆': [106.54, 29.59],
                       '台州': [121.420757, 28.656386],
                       '南京': [118.78, 32.04],
                       '滨州': [118.03, 37.36],
                       '贵阳': [106.71, 26.57],
                       '无锡': [120.29, 31.59],
                       '本溪': [123.73, 41.3],
                       '克拉玛依': [84.77, 45.59],
                       '渭南': [109.5, 34.52],
                       '马鞍山': [118.48, 31.56],
                       '宝鸡': [107.15, 34.38],
                       '焦作': [113.21, 35.24],
                       '句容': [119.16, 31.95],
                       '北京': [116.46, 39.92],
                       '徐州': [117.2, 34.26],
                       '衡水': [115.72, 37.72],
                       '包头': [110, 40.58],
                       '绵阳': [104.73, 31.48],
                       '乌鲁木齐': [87.68, 43.77],
                       '枣庄': [117.57, 34.86],
                       '杭州': [120.19, 30.26],
                       '淄博': [118.05, 36.78],
                       '鞍山': [122.85, 41.12],
                       '溧阳': [119.48, 31.43],
                       '库尔勒': [86.06, 41.68],
                       '安阳': [114.35, 36.1],
                       '开封': [114.35, 34.79],
                       '济南': [117, 36.65],
                       '德阳': [104.37, 31.13],
                       '温州': [120.65, 28.01],
                       '九江': [115.97, 29.71],
                       '邯郸': [114.47, 36.6],
                       '临安': [119.72, 30.23],
                       '兰州': [103.73, 36.03],
                       '沧州': [116.83, 38.33],
                       '临沂': [118.35, 35.05],
                       '南充': [106.110698, 30.837793],
                       '天津': [117.2, 39.13],
                       '富阳': [119.95, 30.07],
                       '泰安': [117.13, 36.18],
                       '诸暨': [120.23, 29.71],
                       '郑州': [113.65, 34.76],
                       '哈尔滨': [126.63, 45.75],
                       '聊城': [115.97, 36.45],
                       '芜湖': [118.38, 31.33],
                       '唐山': [118.02, 39.63],
                       '平顶山': [113.29, 33.75],
                       '邢台': [114.48, 37.05],
                       '德州': [116.29, 37.45],
                       '济宁': [116.59, 35.38],
                       '荆州': [112.239741, 30.335165],
                       '宜昌': [111.3, 30.7],
                       '义乌': [120.06, 29.32],
                       '丽水': [119.92, 28.45],
                       '洛阳': [112.44, 34.7],
                       '秦皇岛': [119.57, 39.95],
                       '株洲': [113.16, 27.83],
                       '石家庄': [114.48, 38.03],
                       '莱芜': [117.67, 36.19],
                       '常德': [111.69, 29.05],
                       '保定': [115.48, 38.85],
                       '湘潭': [112.91, 27.87],
                       '金华': [119.64, 29.12],
                       '岳阳': [113.09, 29.37],
                       '长沙': [113, 28.21],
                       '衢州': [118.88, 28.97],
                       '廊坊': [116.7, 39.53],
                       '菏泽': [115.480656, 35.23375],
                       '合肥': [117.27, 31.86],
                       '武汉': [114.31, 30.52],
                       '大庆': [125.03, 46.58]}

    LF_data = locate.select().where(locate.ID == uuid)
    for data in LF_data:
        ip_locate = data.IP_info.split(',')[1] if data.IP_info.split(',')[0] == '' and data.IP_info != '' else \
        data.IP_info.split(',')[0]
        if ip_locate.split('|')[0] == '中国':
            for place in ip_locate.split('|'):
                if '市' in place:
                    check_info['position'].append({"name":place[:-1], "value": "ip来源"})
                    check_info['geoCoordMap'][str(place[:-1])] = city_coordinate[str(place[:-1])] if place[
                                                                                     :-1] in city_coordinate.keys() else []
        if ip_locate.split('|')[0] in ['香港', '澳门']:
            pass

        if data.reg_whois_city != "":
            check_info['position'].append({"name": data.reg_whois_city, "value": "whois来源"})
            check_info['geoCoordMap'][str(data.reg_whois_city)] = city_coordinate[
                                            str(data.reg_whois_city)] if data.reg_whois_city in city_coordinate.keys() else []

        if data.reg_postal_city != "":
            check_info['position'].append({"name": data.reg_postal_city, "value": "postal来源"})
            check_info['geoCoordMap'][str(data.reg_postal_city)] = city_coordinate[
                                             str(data.reg_postal_city)] if data.reg_postal_city in city_coordinate.keys() else []

        if data.reg_phone_province != "":
            check_info['position'].append({"name": data.reg_phone_province, "value": "phone来源"})
            check_info['geoCoordMap'][str(data.reg_phone_city)] = city_coordinate[
                                            str(data.reg_phone_city)] if data.reg_phone_city in city_coordinate.keys() else []


    # base_info
    BI_data_judge = domain_index.select(domain_index.judge_flag).where(domain_index.ID == uuid)
    BI_data_judge1 = malicious_info.select(malicious_info.influence).where(malicious_info.ID == uuid)

    type = {0: "默认", 1: "良性", -2: "赌博", -3: "色情", -1: "恶意未分类"}
    m_judge = 1001
    influence = 0
    for data in BI_data_judge:
        m_judge = data.judge_flag
        if data.judge_flag in type.keys():
            check_info['base_info']['area'] = type[data.judge_flag]
        else:
            check_info['base_info']['area'] = "未定义"
    for data in BI_data_judge1:
        check_info['base_info']['score'] = data.influence
        influence = data.influence


    #  same_event
    if m_judge in type.keys() and m_judge < 0:
        check_info['same_event'][0]['seen'] = "true"
        check_info['same_event'][0]['samet'] = type[m_judge]
        check_info['same_event'][0]['malicious_info'] = []
        check_info['same_event'][0]['malicious_info'].append({"area":type[m_judge]})
        BI_data_tend = malicious_type.select(malicious_type.tend_avg).where(malicious_type.type == type[m_judge])
        if BI_data_tend:
            check_info['same_event'][0]['xsame']=[]
            for data in BI_data_tend:
                i = 1
                for tend in data.tend_avg.split(","):
                    check_info['same_event'][0]['xsame'].append({"x":"第"+str(i)+"次", "y":tend})
                    i += 1
                check_info['same_event'][0]['samen'] = data.tend_avg.split(",")[i-2]
        else:
            check_info['same_event'][0]['xsame'] = []
            check_info['same_event'][0]['samen'] = 0
    else:
        check_info['same_event'][0]['seen'] = "false"

    # analysis
    if m_judge in type.keys() and m_judge < 0:
        check_info['analysis'][0]['seen'] = "true"
        check_info['analysis'][0]['dnsanay'] = keyword
        check_info['analysis'][0]['dnshot'] = influence
        check_info['analysis'][0]["dnsno"] = ""
        check_info['analysis'][0]["dnsloc"] = ""
        check_info['analysis'][0]["powerData"] = []
        BI_other = other_info.select(other_info.Alex, other_info.appears_location).where(other_info.ID == uuid)
        for data in BI_other:
            check_info['analysis'][0]["dnsno"] = data.Alex
            check_info['analysis'][0]["dnsloc"] = data.appears_location

        RES_data = whois.select(whois.reg_phone, whois.reg_name, whois.reg_email, whois.org_name).where(
            whois.ID == uuid)
        for data in RES_data:
            check_info['analysis'][0]["powerData"].append({"powername": "姓名","powerinfo": data.reg_name})
            check_info['analysis'][0]["powerData"].append({"powername": "邮箱", "powerinfo": data.reg_email})
            check_info['analysis'][0]["powerData"].append({"powername": "电话", "powerinfo": data.reg_phone})
            check_info['analysis'][0]["powerData"].append({"powername": "公司", "powerinfo": data.org_name})
        address_data = locate.select(locate.province, locate.city, locate.street).where(locate.ID == uuid)
        for data in address_data:
            check_info['analysis'][0]["powerData"].append({"powername": "地址", "powerinfo":  data.province + data.city + data.street})

        check_info['analysis'][0]["dnsherf"] = ""
        url_data = malicious_info.select(malicious_info.malicious_link).where(malicious_info.ID == uuid)
        for data in url_data:
            if data.malicious_link != "":
                for id in url_data.split(","):
                    url_data_s = malicious_link.select(malicious_link.type,malicious_link.url).where(malicious_link.url_id == int(id))
                    for k in url_data_s:
                        if k.type in type.keys():
                            check_info['analysis'][0]["dnsherf"] = check_info['analysis'][0]["dnsherf"]+k.url+" "+type[k.type]+"|"


    else:
        check_info['analysis'][0]['seen'] = "false"

    return json.dumps(check_info, cls=DateEncoder, ensure_ascii=False)















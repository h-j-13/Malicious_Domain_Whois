#! coding:utf-8

"""
    基本SQL语句
"""

import MySQLdb


full_data_id="(select ID from domain_index where (other_info_flag!=3 or other_info_flag!=4)\
                and whois_flag=1 and locate_flag>0)"


def has_alex_rank():
    """
        分析两类域名在 有 alexa排名时的差异
    """
    sql="select count(*),web_judge_result from domain_index d,other_info o where d.ID=o.ID and o.Alex!=\"--\" and o.Alex!='' and d.ID in %s group by web_judge_result"%full_data_id
    con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys")
    cur=con.cursor()
    # print sql
    cur.execute(sql)
    result=cur.fetchall()
    to_return={"mal&&alex":0,"alex":0}
    for item in result:
        if item[1]==2 or item[1]==3:
            to_return['mal&&alex']+=item[0]
        elif item[1]==1:
            to_return['alex']+=item[0]
    return to_return

def no_alex_rank():
    """
        分析两类域名 无 alexa排名时的差异
    """
    con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys")
    cur=con.cursor()
    sql="select count(*),web_judge_result from domain_index d,other_info o where d.ID=o.ID and o.Alex=\"--\" and d.ID in %s group by web_judge_result"%full_data_id
    cur.execute(sql)
    result=cur.fetchall()
    to_return={"mal&&noalex":0,"noalex":0}
    for item in result:
        if item[1]==2 or item[1]==3:
            to_return['mal&&noalex']+=item[0]
        elif item[1]==1:
            to_return['noalex']+=item[0]
    return to_return


def diff_location():
    """
        分析两类域名在地理位置 不重合 时的差异
    """
    con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys")
    cur=con.cursor()
    location_diff="select count(*),judge_flag from domain_index d,locate l where d.ID=l.ID and d.locate_flag>0 and l.cmp>0 group by d.judge_flag "
    cur.execute(location_diff)
    result=cur.fetchall()
    item=eval(str(result))
    # print item
    to_return={"mal&&diff":0,"diff":0}
    for i in item:
        if i[1]==2 or i[1]==3:
            to_return['mal&&diff']+=i[0]
        to_return['diff']+=i[0]
    return to_return

def same_location():
    """
        分析两类域名在地理位置 重合 时的差异
    """
    con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys")
    cur=con.cursor()
    sql="select count(*),judge_flag from domain_index d,locate l where d.ID=l.ID and d.ID in %s and l.cmp<=0 group by d.judge_flag"%full_data_id
    # print sql
    cur.execute(sql)
    result=cur.fetchall()
    to_return={"mal&&same":0,"same":0}
    for i in result:
        if i[1]==2 or i[1]==3:
            to_return['mal&&same']+=i[0]
        if i[1]!=4:
            to_return['same']+=i[0]
    return to_return

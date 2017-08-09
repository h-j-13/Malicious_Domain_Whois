#! coding:utf-8

import MySQLdb
import BaseSQL
import Utilities
import config


def mal_probability_on_keywords(domain):
    """
        恶意概率 on 恶意关键词
    """
    con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys",charset='utf8')
    cur=con.cursor()
    sql="select judge_grade from malicious_info where ID=%s"%str(hash(domain))
    try:
        cur.execute(sql)
        result=cur.fetchall()
        f=float(str((result[0][0])))
        return 0.5+0.1*f
    except Exception,e:
        print "[ERROR]: ","fail to get mal_probability_on_keywords of %s"%domain
        return 0.5

def mal_probability_on_http30x(domain):
    """
        恶意概率 on 重定向
    """
    con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys",charset='utf8')
    cur=con.cursor()
    sql="select HTTPcode from malicious_info where ID=%s"%str(hash(domain))
    try:
        cur.execute(sql)
        r=cur.fetchall()
        code=int(r[0][0])
        if code>=300 and code<400:
            return 1
        else:
            return 0.5
    except Exception,e:
        print "[ERROR]: ","fail to get mal_probability_on_http30x of %s"%domain
        return 0.5

def mal_probability_on_alexa(domain):
    """
        恶意概率 on alexa排名
        (不建议纳入模型,因为alexa排名并不准确,需要确认其有效性)
    """
    con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys",charset='utf8')
    cur=con.cursor()
    sql="select Alex from other_info where ID=%s"%(hash(domain))
    try:
        cur.execute(sql)
        result=cur.fetchall()
        if result[0][0]=="--":
            return config.probability_no_alexa_rank
        else:
            return config.probability_has_alexa_rank
    except Exception,e:
        print "[ERROR]: ","fail to get mal_probability_on_alexa of %s"%domain
        return 0.5

def mal_probability_on_locate(domain):
    """
        恶意概率 on 地理位置比对
    """
    con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys",charset='utf8')
    cur=con.cursor()
    sql="select cmp from locate where ID=%s"%(hash(domain))
    try:
        cur.execute(sql)
        result=cur.fetchall()
        cmp=result[0][0]
        if cmp>0:
            return config.probability_locate_match
        else:
            return config.probability_locate_diff
    except:
        return 0.5

def mal_probability_on_registrar(domain):
    """
        恶意概率 on 注册商
    """
    registrar=Utilities.get_domain_registrar(domain)
    num=Utilities.get_registrar_num(registrar)
    if num < config.min_registrar_num_to_consider:
        return 0.5
    else:
        return Utilities.get_probability_on_registrar(registrar)

def mal_probability_on_email_suffix(domain):
    """
        恶意概率 on 注册者邮箱后缀
    """
    email=Utilities.get_email(domain)
    if email == "":
        return 0.5
    suffix=Utilities.get_email_suffix(email)
    if suffix == "":
        return 0.5
    summary=Utilities.diff_reg_email_suffix(suffix)
    if summary['mal&&suffix_match']+summary['nomal&&suffix_match'] < 50:
        return 0.5
    else:
        return float(summary['mal&&suffix_match'])/(float(summary['nomal&&suffix_match'])+float(summary['mal&&suffix_match']))

def get_domain_features(domain):
    f=[mal_probability_on_keywords(domain),
        mal_probability_on_http30x(domain),
        mal_probability_on_alexa(domain),
        mal_probability_on_locate(domain),
        mal_probability_on_registrar(domain),
        mal_probability_on_email_suffix(domain)]
    return f

def main(domain='95588tpi.cc'):
    print mal_probability_on_keywords(domain)
    print mal_probability_on_http30x(domain)
    print mal_probability_on_alexa(domain)
    print mal_probability_on_locate(domain)
    print mal_probability_on_registrar(domain)
    print mal_probability_on_email_suffix(domain)

if __name__=="__main__":
    main()

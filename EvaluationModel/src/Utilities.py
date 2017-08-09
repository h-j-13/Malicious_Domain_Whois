#!coding:utf-8

import MySQLdb
import BaseSQL

def get_domain_registrar(domain):
    con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys",charset='utf8')
    cur=con.cursor()
    try:
        cur.execute("select sponsoring_registrar from whois where ID=%s"%(hash(domain)))
        result=cur.fetchall()
        return result[0][0]
    except Exception,e:
        print "[ERROR]: ","fail to get registrar of %s"%domain
        return None


def get_registrar_num(registrar,cache={}):
    if registrar in cache.keys():
        return cache[registrar]
    con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys",charset='utf8')
    cur=con.cursor()
    try:
        sql="select count(*) from whois where sponsoring_registrar=\"%s\" and ID in %s"%(registrar,BaseSQL.full_data_id)
        # print sql
        cur.execute(sql)
        result=cur.fetchall()
        cache[registrar]=result[0][0]
        return result[0][0]
    except Exception,e:
        print "[ERROR]: ","fail to get domain num under %s"%registrar
        cache[registrar]=None
        return None

def get_probability_on_registrar(registrar,cache={}):
    if registrar in cache.keys():
        return cache[registrar]
    con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys",charset='utf8')
    cur=con.cursor()
    sql="select count(*) from whois where sponsoring_registrar=\"%s\" and ID in%s"%(registrar,BaseSQL.full_data_id)
    cur.execute(sql)
    total=cur.fetchall()
    sql="select count(*) from whois w,domain_index d where w.ID=d.ID and w.ID in %s and w.sponsoring_registrar=\"%s\" and (d.judge_flag=3 or d.judge_flag=2)"%(BaseSQL.full_data_id,registrar)
    cur.execute(sql)
    mal=cur.fetchall()
    p=float(mal[0][0])/float(total[0][0])
    cache[registrar]=p
    return p

def get_email(domain):
    sql="select reg_email from whois where ID=%s"%(str(hash(domain)))
    con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys")
    cur=con.cursor()
    try:
        cur.execute(sql)
        result=cur.fetchall()
        return result[0][0]
    except Exception,e:
        print "[ERROR]: ","fail to get reg_email of %s"%domain
        return ""

def get_email_suffix(email):
    if email=="":
        return ""
    else:
        return email[email.find('@'):]

def diff_reg_email_suffix(email_suffix,cache={}):
    """
        设置缓存机制,提高速度
    """
    suffix=email_suffix
    if suffix in cache.keys():
        return cache[suffix]
    else:
        sql="select count(*),judge_flag from domain_index d,whois w where d.ID=w.ID and d.ID in (%s) and w.reg_email REGEXP '%s' group by judge_flag;"%(BaseSQL.full_data_id,suffix)
        r={'mal&&suffix_match':0,'nomal&&suffix_match':0}
        try:
            con = MySQLdb.connect("172.26.253.3", "root", "platform","malicious_domain_sys")
            cur=con.cursor()
            cur.execute(sql)
            result=cur.fetchall()
            for item in result:
                if item[1]==2 or item[1]==3:
                    r['mal&&suffix_match']+=int(item[0])
                else:
                    r['nomal&&suffix_match']+=int(item[0])
            cache[suffix]=r
            return r
        except:
            raise


def main():
    d='95588tpi.cc'
    # registrar=get_domain_registrar(d)
    # num=get_registrar_num(registrar)
    # p=get_probability_on_registrar(registrar)
    # print registrar,num,p
    print get_email(d)

if __name__=="__main__":
    main()

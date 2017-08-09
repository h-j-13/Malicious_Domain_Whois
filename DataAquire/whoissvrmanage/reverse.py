#!/usr/bin/python
# encoding:utf-8
"""
用来获取whois域名的IP地址
"""
from datetime import datetime
import dns.resolver
from db_manage import MySQL
from verify_port import port_available_flag as get_port_flag



def judege_ips_equal(domain_latest_ips,source_ips):
    """判断两个ip列表是否相同
    参数
        source_ips: list 数据库原有IP,不为空
        domain_latest_ips: list 域名最新解析的ip，不为空
    返回值
        True/False: boolean 两个列表是否相同
    """
    return set(domain_latest_ips).issubset(set(source_ips))

def merge_ips(source_ips,domain_latest_ips):
    
    return list(set(source_ips+domain_latest_ips))


def get_svr_from_db():
    """从数据库中获取服务器域名地址和已有IP
    
    返回值
        svr_ips: list 待查询IP的whois服务器域名和已有ip列表
        
    """
    db = MySQL()
    sql = 'SELECT svr_name,ip FROM svr_ip'
    db.query(sql)
    svr_ips = db.fetchAllRows()
    db.close()
    return list(svr_ips)


def domain2ip(domain):
    """
    域名解析为IP列表
    参数
        domain: string 待解析的域名
    
    返回值
        ips: list 域名解析后的ip列表
    """
    ips = []
    res = dns.resolver.Resolver()
    res.nameservers = ['8.8.8.8','8.8.4.4','156.154.70.1','156.154.71.1','208.67.222.222','208.67.220.220','209.244.0.3']
    
    try:
        domain_ip = res.query(domain,'A')
        for i in domain_ip:
            ips.append(i.address)
    except:
        ips = []
    return ips

                
def get_latest_svr_ips(domain_latest_ips,source_ips):
    if not domain_latest_ips:
        return False
    if source_ips is None:
        return domain_latest_ips
    else:
        if judege_ips_equal(domain_latest_ips,source_ips.split(',')):
            return False
        else:
            return merge_ips(domain_latest_ips,source_ips.split(','))
            
def get_svr_ip():
    """
    获取服务器的IP地址，并与已有ip比对,最后更新数据库
    """
    print str(datetime.now()),'开始解析whois服务器域名'
    svr_addr = get_svr_from_db() # 得到要查询的列表
    sql = 'UPDATE svr_ip SET ip="%s",port_available="%s" WHERE svr_name="%s"'
    db = MySQL()
    for addr in svr_addr:
        ips = domain2ip(addr[0])
        latest_ips = get_latest_svr_ips(ips,addr[1])
        if latest_ips:
            port_flag = get_port_flag(latest_ips)
            print addr[0],str(latest_ips),port_flag
            db.update(sql % (','.join(latest_ips),port_flag,addr[0]))
    db.close()
    print str(datetime.now()),'结束解析whois服务器域名'

#if __name__== '__main__':
 #   get_svr_ip()

#!/usr/bin/python
# encoding:utf-8
"""
验证其43端口是否开放
"""

import socket
from db_manage import MySQL
from datetime import datetime

def get_svr_from_db():
    """从数据库中获取服务器域名地址和已有IP
    
    返回值
        svr_ips: list 待查询IP的whois服务器域名和已有ip列表
        
    """
    db = MySQL()
    sql = 'SELECT svr_name,ip FROM svr_ip WHERE ip IS NOT NULL'
    db.query(sql)
    svr_ips = db.fetchAllRows()
    db.close()
    return list(svr_ips)



def connect_port(ip):
    """
    使用socket与ip的43端口进行连接
    参数
        ip: string 需要验证的ip
    返回值
        True/False: boolean 是否可连接
    """
    port = 43 # whois服务器端口号
    s = socket.socket()
    s.settimeout(3)
    socket_no = s.connect_ex((ip, port),)
    s.close()
    if socket_no == 0:  # 连接成功
        return True
    else:
        return False
        
def verify_ip_whois():
    """
    验证ip地址的whois端口号是否开放
    """
    print str(datetime.now()),'开始验证IP的whois端口'
    ips = get_svr_from_db()
    db = MySQL()
    sql = 'UPDATE svr_ip SET port_available = "%s" WHERE svr_name = "%s"'
    for value in ips:
        available_flag = port_available_flag(value[1].split(','))
        # print value[0],available_flag
        db.update(sql % (available_flag,value[0]))
    db.close()
    print str(datetime.now()),'结束验证IP的whois端口'


def port_available_flag(ips):
    """
    批量验证端口是否开放,并生成标记位
    """
    available_flag = ''
    for ip in ips:
        if connect_port(ip):
            available_flag += '1'
        else:                      
            if connect_port(ip):  # 重复验证一次
                available_flag += '1'
            else:
                available_flag += '0'
    return available_flag



#if __name__ == '__main__':
 #   verify_ip_whois()

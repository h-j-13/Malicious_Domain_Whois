# !/usr/bin/python
# encoding:UTF-8

# whois信息测试

import datetime
import os
import re
import socket
from domain_status import get_status_value

# import proxy_ip
import socks


# _proxy_ip = proxy_ip.ProxyIP()


# 与whois服务连接获取whois信息
def get_recv_info(domain, whois_srv):
    if whois_srv == "whois.jprs.jp":
        request_domain = "%s/e" % domain # Suppress Japanese output
    elif domain.endswith(".de") and ( whois_srv == "whois.denic.de" or whois_srv == "de.whois-servers.net" ):
        request_domain = "-T dn,ace %s" % domain # regional specific stuff
    elif whois_srv == "whois.verisign-grs.com" or whois_srv == "whois.crsnic.net":
        request_domain = "=%s" % domain # Avoid partial matches
    else:
        request_domain = domain
    port = 43  # 端口
    buffer_size = 1024  # 每次返回数据大小
    data_result = ""
    try:
        tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(20)
        tcpCliSock.connect((whois_srv, port))
        tcpCliSock.send(request_domain + '\r\n')
    except socket.error as e:
        if str(e).find("timed out") != -1:  # 连接超时
            return "ERROR -1"
        elif str(e).find("Temporary failure in name resolution") != -1:
            return "ERROR -2"
        else:
            return "ERROR OTHER"

    while True:
        try:
            data_rcv = tcpCliSock.recv(buffer_size)
        except socket.error as e:
            return "ERROR -3"
        if not len(data_rcv):
            return data_result  # 返回查询结果
        data_result = data_result + data_rcv  # 每次返回结果组合

def flag_manage(domain_whois):
    result = ''
    result += '0' if domain_whois['reg_name'] == '' else '1'
    result += '0' if domain_whois['reg_phone'] == '' else '1'
    result += '0' if domain_whois['reg_email'] == '' else '1'
    result += '0' if domain_whois['org_name'] == '' else '1'
    result += '0' if domain_whois['creation_date'] == '' else '1'
    result += '0' if domain_whois['expiration_date'] == '' else '1'
    result += '0' if domain_whois['updated_date'] == '' else '1'
    result += '0' if domain_whois['name_server'] == '' else '1'
    result += '0' if domain_whois['sponsoring_registrar'] == '' else '1'
    return result

def data_deal_tt(data, domain_whois):
    sign_not_exist_list = ['No match for', 'Available\nDomain', 'The queried object does not exist:', \
           'Requested Domain cannot be found', 'The queried object does not exist: Domain name', \
           'No Data Found', 'Domain Status: No Object Found', 'Domain not found.',
           'no matching objects found', \
           'No matching record.', 'No match', '\" is available for registration', '\"  not found', \
           'This domain name has not been registered.', 'NOT FOUND', 'Status: Not Registered', \
           'The queried object does not exists', 'Not found:', 'Object does not exists'
           ]
    for sign_not_exist in sign_not_exist_list:
        if data.find(sign_not_exist) != -1:
            domain_whois['domain_status'] = 'NOTEXIST'
            return domain_whois

    status = ''
    name_server = ''

    pattern = re.compile(r'(Last updated Date ?:.*|Last Updated On ?:.*\
|Update Date ?:.*|Registrant Phone ?:.*|Registrant Name ?:.*\
|Registrant Organization ?:.*|Registrant Email ?:.*\
|Registrant Phone Number ?:.*|Updated Date ?:.*\
|Creation Date ?:.*|Expiration Date ?:.*|Expires On ?:.*\
|Creation date ?:.*|Created Date ?:.*|Registrant Organisation ?:.*\
|Registrant E-mail ?:.*|Update date ?:.*|Created On ?:.*\
|Expiration date ?:.*|Updated date ?:.*|Updated On ?:.*\
|Registrant Firstname ?:.*\nRegistrant Lastname ?:.*|Expiry Date ?:.*\
|Create Date ?:.*|Status:.*|Registrar:.*|Name Server:.*\
|Nameservers:.*|Registration Date:.*|creation date:.*)')

    for match in pattern.findall(data):

        if match.split(':')[0].strip() == 'Registrant Phone' or \
                        match.split(':')[0].strip() == 'Registrant Phone Number':
            domain_whois['reg_phone'] = match.split(':')[1].strip()

        elif match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()

        elif match.find('Firstname') != -1 and match.find('Lastname') != -1:
            reg_name = match.split('\n')[0].split(':')[1].strip() + ' ' + \
                       match.split('\n')[1].split(':')[1].strip()
            domain_whois['reg_name'] = match.split(':')[1].strip()

        elif match.split(':')[0].strip() == 'Registrant Email' or \
                        match.split(':')[0].strip() == 'Registrant E-mail':
            domain_whois['reg_email'] = match.split(':')[1].strip()

        elif match.split(':')[0].strip() == 'Registrant Organization' or \
                        match.split(':')[0].strip() == 'Registrant Organisation':
            domain_whois['org_name'] = match.split(':')[1].strip()

        elif match.split(':')[0].strip() == 'Updated Date' or \
                        match.split(':')[0].strip() == 'Update Date' or \
                        match.split(':')[0].strip() == 'Last updated Date' or \
                        match.split(':')[0].strip() == 'Update date' or \
                        match.split(':')[0].strip() == 'Last Updated On' or \
                        match.split(':')[0].strip() == 'Updated date' or \
                        match.split(':')[0].strip() == 'Updated On':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()

        elif match.split(':')[0].strip() == 'Creation Date' or \
                        match.split(':')[0].strip() == 'Creation date' or \
                        match.split(':')[0].strip() == 'Created Date' or \
                        match.split(':')[0].strip() == 'Created On' or \
                        match.split(':')[0].strip() == 'Create Date' or \
                        match.split(':')[0].strip() == 'creation date' or\
                        match.find('Registration Date:') != -1:
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()

        elif match.split(':')[0].strip() == 'Expiration Date' or \
                        match.split(':')[0].strip() == 'Expiration date' or \
                        match.split(':')[0].strip() == 'Expiry Date' or \
                        match.split(':')[0].strip() == 'Expires On':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()

        elif match.find('Status:') != -1:
            status += match.split(':', 1)[1].strip().split(' ')[0].strip()
            status += ';'

        elif match.find('Registrar:') != -1:
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()

        elif match.find('Name Server:') != -1 or \
                match.find('Nameservers:') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['domain_status'] = status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def data_deal(data, domain_whois):
    if data.find('No entries found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(Owner:.*(\n.*)+?\n\n|Registration date:.*|Status:.*|DNS Servers:.*(\n.*)\n\n)')
    for match in pattern.findall(data):
        match =  match[0]
        if match.find('Owner:') != -1:
            domain_whois['reg_name'] = match.split('\n')[2].strip()
            for line in match.split('\n'):
                if line.find('Phone:') != -1:
                    domain_whois['reg_phone'] = line.split(':')[1].strip()
                elif line.find('Email:') != -1:
                    domain_whois['reg_email'] = line.split(':')[1].strip()
        elif match.find('Registration date:') != -1:
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.find('Status:') != -1:
            domain_status += match.split(':')[1].strip()
        elif match.find('DNS Servers:') != -1:
            for line in match.split('\n'):
                if len(line) > 2 and line.find('DNS Servers:') == -1:
                    name_server += line.strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

if __name__ == '__main__':

    domain = 'googdsadale.sm'
    whois_server = 'whois.nic.sm'

    domain_whois = {"domain": "",  # 域名
                    "flag": 0,  # 状态标记
                    "domain_status": "",  # 域名状态
                    "sponsoring_registrar": "",  # 注册商
                    "top_whois_server": "",  # 顶级域名服务器
                    "sec_whois_server": "",  # 二级域名服务器
                    "reg_name": "",  # 注册姓名
                    "reg_phone": "",  # 注册电话
                    "reg_email": "",  # 注册email
                    "org_name": "",  # 注册公司名称
                    "creation_date": "",  # 创建时间
                    "expiration_date": "",  # 到期时间
                    "updated_date": "",  # 更新时间
                    "insert_time": "",  # 信息插入时间
                    "details": "",  # 细节
                    "name_server": "",  # 域名服务器
                    "hash_value": 0,  # 哈希值
                    }
    domain_whois['domain'] = domain
    domain_whois['top_whois_server'] = whois_server

    data = get_recv_info(domain, whois_server)

    print '-------------------data---------------------'
    print data

    if not data:
        exit()

    print "---------------domain_whois-----------------"
    result = data_deal(data, domain_whois)
    result['insert_time'] = str(datetime.datetime.now()).split('.')[1]
    result['flag'] = flag_manage(result)
    result['details'] = str(data)
    result['domain_status'] = get_status_value(result['domain_status'], result['domain'])
    result['hash_value'] = hash(result['details'])


    print "domain:                      ", result['domain']
    print "domain_status:               ", result['domain_status']
    print "flag:                        ", result['flag']
    print "sponsoring_registrar:        ", result['sponsoring_registrar']
    print "top_whois_server:            ", result['top_whois_server']
    print "sec_whois_server:            ", result['sec_whois_server']
    print "reg_name:                    ", result['reg_name']
    print "reg_phone:                   ", result['reg_phone']
    print "reg_email:                   ", result['reg_email']
    print "org_name:                    ", result['org_name']
    print "updated_date:                ", result['updated_date']
    print "creation_date:               ", result['creation_date']
    print "expiration_date:             ", result['expiration_date']
    print "name_server:                 ", result['name_server']

    print "hash_value:                  ", result['hash_value']
    # print "details", result['details']

    print "--------------------------------------------"

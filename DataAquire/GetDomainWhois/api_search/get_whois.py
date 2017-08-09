# usr/bin/python
# encoding:utf-8

# whois 信息获取，客户端

import json
import re

from whois_connect import GetWhoisInfo
from whois_connect import WhoisConnectException


# 请求信息
def get_whois(domain_info):
    whois_server_first = domain_info['whois_srv']
    func_name = domain_info['func_name']
    domain = domain_info['domain']
    exist = domain_info['exist']

    flag_error = '0'  # 错误标志
    flag_first_error = '000'  # 一级错误
    flag_sec_error = '000'  # 二级错误
    whois_server_sec = ''  # 二级服务器
    whois_details = ''  # 返回数据

    # 可能存在二级服务器
    if func_name == 'com_manage':
        whois_details_first = ''
        try:
            whois_details_first = GetWhoisInfo(domain, whois_server_first).get()
            if xxx_bool(whois_details_first):
                whois_details_first = GetWhoisInfo('=' + domain, whois_server_first).get()
        except WhoisConnectException as e:
            flag_error = '1'
            flag_first_error = bin(int(str(e)))[2:]
            flag_first_error = '0' * (3 - len(flag_first_error)) + flag_first_error

        whois_details_sec = None
        try:
            whois_server_sec = get_sec_server(whois_details_first, domain)
            if whois_server_sec:
                whois_details_sec = GetWhoisInfo(domain, whois_server_sec).get()
        except WhoisConnectException as e:
            flag_error = '1'
            flag_sec_error = bin(int(str(e)))[2:]
            flag_sec_error = '0' * (3 - len(flag_sec_error)) + flag_sec_error
            whois_details = whois_details_first
        else:
            whois_details = whois_details_sec
    else:
        try:
            whois_details = GetWhoisInfo(domain, whois_server_first).get()
        except WhoisConnectException as e:
            flag_error = '1'
            flag_first_error = bin(int(str(e)))[2:]
            flag_first_error = '0' * (3 - len(flag_first_error)) + flag_first_error
            flag_sec_error = '000'

    whois_result = {
            'domain': domain,
            'top_whois_server': whois_server_first,
            'sec_whois_server': whois_server_sec,
            'whois_details': whois_details,
            'result_flag': '1' + flag_error + flag_first_error + flag_sec_error,  # 结果标志
            'func_name': func_name,
            'exist': exist
    }
    return whois_result

# 用来判断com_manage函数中，得到的whois信息是否包含xxx标志，若包括则需要重新发送
def xxx_bool(data):
    if data.find('\"xxx\"') != -1 and data.find('\"=xxx\"') != -1:
        return True
    else:
        return False

# 提取com_manage中whois信息中的，二级whois服务器名称
def get_sec_server(data, domain):
    if not data:
        return False
    if data.find("Domain Name: %s" % domain.upper()) != -1:
        pos = data.find("Domain Name: %s" % domain.upper())
        data = data[pos:]
        pattern = re.compile(r"Whois Server:.*|WHOIS Server:.*")
        sec_whois_server = ''
        for match in pattern.findall(data):
            if match.find('Server:') != -1:
                sec_whois_server = match.split(':')[1].strip()
        return False if sec_whois_server == '' else sec_whois_server
    elif data.find('Registrar WHOIS Server:') != -1:  # ws二级服务器
        pattern = re.compile(r'Registrar WHOIS Server:.*?')
        sec_whois_server = ''
        for match in pattern.findall(data):
            if match.find('Server:') != -1:
                sec_whois_server = match.split(':')[1].strip()
        return False if sec_whois_server == '' else sec_whois_server
    else:
        return False

if __name__ == '__main__':
    pass

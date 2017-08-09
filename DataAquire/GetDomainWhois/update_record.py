#!/usr/bin/python
# encoding:utf-8

#
# 添加或更新域名记录
# @author wangkai 
# 

from static import Static
from whois_info_deal.info_deal import get_deal_result


# 更新域名记录
def update_record(recv_info_from_client):
    result_flag = recv_info_from_client['result_flag']
    func_name = recv_info_from_client['func_name']
    exist = recv_info_from_client['exist']

    domain_whois = {
        'domain_hash': hash(recv_info_from_client['domain']),  # 域名哈希值
        "domain": recv_info_from_client['domain'],  # 域名
        "flag": 0,  # 状态标记
        "domain_status": "",  # 域名状态
        "sponsoring_registrar": "",  # 注册商
        "top_whois_server": recv_info_from_client['top_whois_server'],  # 顶级域名服务器
        "sec_whois_server": recv_info_from_client['sec_whois_server'],  # 二级域名服务器
        "reg_name": "",  # 注册姓名
        "reg_phone": "",  # 注册电话
        "reg_email": "",  # 注册email
        "org_name": "",  # 注册公司名称
        "creation_date": "",  # 创建时间
        "expiration_date": "",  # 到期时间
        "updated_date": "",  # 更新时间
        "insert_time": Static.get_now_time(),  # 信息插入时间
        "details": recv_info_from_client['whois_details'],  # 细节
        "name_server": "",  # 域名服务器
        "whois_hash": 0,  # whois信息哈希值
    }
    domain_whois = get_deal_result(domain_whois, func_name, result_flag)
    if not domain_whois:
        return
    # 第一次跑数据
    if exist:
        # 数据库中存在该记录
        if not is_exist(domain_whois.get('domain_status')):
            # 域名为未存在
            Static.whois_db.delete_whois_info(domain_whois['domain'])
        else:
            Static.whois_db.update_whois_info(**domain_whois)
    else:
        # 数据库中不存在该记录
        if is_exist(domain_whois.get('domain_status')):
            # 域名存在
            Static.whois_db.db_whois_insert(**domain_whois)
    return domain_whois

# 更新不存在tld记录的域名信息
def update_not_tld_record(domain, exist):
    if exist:
        Static.whois_db.set_whois_flag(domain, -99)
    else:
        domain_whois = {
            'domain_hash': hash(domain),  # 域名哈希值
            "domain": domain,  # 域名
            "flag": -99,  # 状态标记
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
            "insert_time": Static.get_now_time(),  # 信息插入时间
            "details": "",  # 细节
            "name_server": "",  # 域名服务器
            "whois_hash": 0,  # whois信息哈希值
        }
        Static.whois_db.db_whois_insert(**domain_whois)

# 更新不存在处理函数的域名信息
def update_not_deal_method(domain, exist):
    if exist:
        Static.whois_db.set_whois_flag(domain, -98)
    else:
        domain_whois = {
            'domain_hash': hash(domain),  # 域名哈希值
            "domain": domain,  # 域名
            "flag": -98,  # 状态标记
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
            "insert_time": Static.get_now_time(),  # 信息插入时间
            "details": "",  # 细节
            "name_server": "",  # 域名服务器
            "whois_hash": 0,  # whois信息哈希值
        }
        Static.whois_db.db_whois_insert(**domain_whois)

# 判断域名时候存在
def is_exist(domain_status):
    return False if domain_status == '29' else True

#!/usr/bin/env python
# encoding:utf-8

"""
    SQL 语句生成
======================

version   :   1.0
author    :   @`13
time      :   2017.3.23
"""


# SQL语句生成及优化
class SQL_generate:
    """
    SQL语句优化类
    """

    def __init__(self):
        self.note = "SQL_refactor类 为 <malicious_domain_sys> 系统专用,请勿混用"

    @staticmethod
    def GET_WHOIS_INFO(domain, column_name, table_name):
        """
        :param domain: 域名
        :param comm_name: 需要获取的字段名
        :return: 生成获取域名whois信息的SQL
                 失败返回 None
        """
        SQL = """SELECT """
        if type(column_name) == str:
            SQL += """ `{cn}`""".format(cn=column_name)
        elif type(column_name) == list:
            for column in column_name:
                if type(column) == str:
                    SQL += """`{cn}`, """.format(cn=column)
                else:
                    return None
            SQL = SQL[:-2]
        else:
            return None
        SQL += """ FROM {T}""".format(T=table_name)
        SQL += """ WHERE ID = {hash}""".format(hash=hash(domain))
        return SQL

    @staticmethod
    def WHOWAS_TRANSFORM(whowas_table_name, whois_table_name, domain):
        """
        :return: whois -> whowas 语句
        """
        SQL = """INSERT INTO {whowas} SELECT * FROM {whois} WHERE ID = {HASH}""".format(
            whowas=whowas_table_name, whois=whois_table_name, HASH=hash(domain))
        return SQL

    @staticmethod
    def WHOIS_INSERT(whois_dict, whois_table_name):
        """
        :param whois_dict: whois 信息字典
        :param whois_table_name: whois表名
        :return: 插入whois表的SQL语句
        """
        SQL = """REPLACE INTO `{whoisTable}` set """.format(whoisTable=whois_table_name)
        SQL += """`ID` = '{Value}', """.format(Value=hash(whois_dict['domain']))
        SQL += """`domain` = '{Value}', """.format(Value=whois_dict['domain'])
        SQL += """`tld` = '{Value}', """.format(Value=whois_dict['tld'])
        SQL += """`flag` = {Value}, """.format(Value=whois_dict['flag'])
        SQL += """`domain_status` = '{Value}', """.format(Value=whois_dict['domain_status'])
        SQL += """`sponsoring_registrar` = '{Value}', """.format(Value=whois_dict['sponsoring_registrar'])
        SQL += """`top_whois_server` = '{Value}', """.format(Value=whois_dict['top_whois_server'])
        SQL += """`sec_whois_server` = '{Value}', """.format(Value=whois_dict['sec_whois_server'])
        SQL += """`reg_name` = '{Value}', """.format(Value=whois_dict['reg_name'])
        SQL += """`reg_phone` = '{Value}', """.format(Value=whois_dict['reg_phone'])
        SQL += """`reg_email` = '{Value}', """.format(Value=whois_dict['reg_email'])
        SQL += """`org_name` = '{Value}', """.format(Value=whois_dict['org_name'])
        SQL += """`name_server` = '{Value}', """.format(Value=whois_dict['name_server'])
        SQL += """`creation_date` = '{Value}', """.format(Value=whois_dict['creation_date'])
        SQL += """`expiration_date` = '{Value}', """.format(Value=whois_dict['expiration_date'])
        SQL += """`updated_date` = '{Value}', """.format(Value=whois_dict['updated_date'])
        SQL += """`details` = '{Value}' """.format(Value=whois_dict['details'])
        return SQL

    @staticmethod
    def PROXY_INFO(proxy_table_name):
        """
        :param proxy_table_name:代理ip表 
        :return: 获取代理socks的SQL语句
        """
        SQL = """SELECT whois_ip, proxy_ip, proxy_port, proxy_mode, message, speed FROM {PorxyTable}""".format(
            PorxyTable=proxy_table_name)
        return SQL

    @staticmethod
    def WHOIS_SRV_INFO(whois_srv_table_name):
        """
        :param whois_srv_table_name:whois服务器表 
        :return: 获取whois服务器ip地址的SQL语句
        """
        SQL = """SELECT svr_name, ip, port_available FROM {SvrIPTable}""".format(
            SvrIPTable=whois_srv_table_name)
        return SQL

    @staticmethod
    def TLD_WHOIS_ADDR_INFO(TLD_table_name):
        """
        :param TLD_table_name: TLD表
        :return: 获取TLD（顶级域）对应的whois服务器的SQL语句
        """
        SQL = """SELECT Punycode, whois_addr FROM {TLDtable}""".format(
            TLDtable=TLD_table_name)
        return SQL

    @staticmethod
    def GET_DOMAIN_FOR_HTTP_STATUS(domain_index_Table, gen_type):
        """
        获取需要判断解析情况的域名的域名
        :param domain_index_Table: TLD表
        :param gen_type: 生成语句类型
        :return: 获取TLD（顶级域）对应的whois服务器的SQL语句
        """
        SQL = """SELECT domain FROM  {T} """.format(
            T=domain_index_Table)
        if gen_type == 0:
            return SQL
        elif gen_type == 1:
            SQL += """ WHERE available = -10 """
        elif gen_type == -1:
            SQL += """ WHERE available != 1 """
        return SQL

    @staticmethod
    def UPDATE_DOMAIN_HTTP_STATUS(domain_Status_Table, domain, available, HTTPcode):
        """
        更新域名的解析情况以及HTTPcode
        :param domain_Status_Table: TLD表
        :return: 获取TLD（顶级域）对应的whois服务器的SQL语句
        """
        SQL = """UPDATE `{T}` SET `HTTPcode`= {hc}, `available`={a} WHERE `ID` = {h} """.format(
            T=domain_Status_Table, hc=HTTPcode, a=available, h=hash(domain))
        return SQL


if __name__ == '__main__':
    # Demo
    print SQL_generate.GET_WHOIS_INFO('baidu.com', ['details', 'flag'], 'whois')
    print SQL_generate.WHOWAS_TRANSFORM('whowas', 'whois', 'baidu.com')

#!/usr/bin/python
# encoding:utf-8

#
# 数据库操作模块
# @author 王凯
#

# import static

# logger = static.logger_db
import peewee
import model
from get_table_name import get_table_num, TableChoiceError


class WhoisDataBase():
    def __init__(self):
        model_list = []  # 模型表
        for i in range(101):
            if i == 0:
                model_list.append('NULL')
            else:
                model_list.append(eval('model.domain_whois_' + str(i)))
        self.model_list = model_list
        self.sign_commit = False

    def connect(self):
        model.db_whois.connect()

    def close(self):
        model.db_whois.close()

    def commit(self):
        self.sign_commit = True
        model.db_whois.commit()
        self.sign_commit = False

    # 查找域名whois信息
    def query_whois_info(self, domain):
        try:
            domain_hash = hash(domain)
            table_num = get_table_num(domain_hash)
            query_results = self.model_list[table_num].select(
            ).where(
                self.model_list[table_num].domain_hash == domain_hash,
                self.model_list[table_num].domain == domain
            )
            return query_results
        except peewee.OperationalError as e:
            raise e
        except TableChoiceError as e:
            raise e

    # 获取没有处理的域名
    # @param table_num 表序号
    # @param tld 域名后缀
    def get_not_deal_domains(self, table_num, finished_tld):
        try:
            result_list = []
            for tld in finished_tld:
                query_results = self.model_list[table_num].select(
                    self.model_list[table_num].domain
                ).where(
                    self.model_list[table_num].flag == -100,
                    self.model_list[table_num].tld == tld
                ).limit(1000)
                for result in query_results:
                    result_list.append(result.domain)
            # str_eval = """self.model_list[table_num].select(
            #         self.model_list[table_num].domain
            # ).where(
            #         self.model_list[table_num].flag == -100).where(
            # """
            # for tld in finished_tld:
            #     str_eval += "self.model_list[table_num].tld == '{tld}'|".format(tld=str(tld))
            # str_eval = str_eval.strip('|') + ').limit(10000)'
            # # print str_eval
            # query_results = eval(str_eval)
            # return query_results
            return result_list
        except peewee.OperationalError as e:
            raise e

    # 更新whois信息
    def update_whois_info(self, **domain_whois):
        try:
            table_num = get_table_num(domain_whois['domain_hash'])
            event = self.model_list[table_num].update(
                flag=domain_whois['flag'],
                domain_status=domain_whois['domain_status'],
                sponsoring_registrar=domain_whois['sponsoring_registrar'],
                top_whois_server=domain_whois['top_whois_server'],
                sec_whois_server=domain_whois['sec_whois_server'],
                reg_name=domain_whois['reg_name'],
                reg_phone=domain_whois['reg_phone'],
                reg_email=domain_whois['reg_email'],
                org_name=domain_whois['org_name'],
                name_server=domain_whois['name_server'],
                creation_date=domain_whois['creation_date'],
                expiration_date=domain_whois['expiration_date'],
                updated_date=domain_whois['updated_date'],
                insert_time=domain_whois['insert_time'],
                details=domain_whois['details'],
                whois_hash=domain_whois['whois_hash']
            ).where(
                self.model_list[table_num].domain_hash == domain_whois['domain_hash'],
                self.model_list[table_num].domain == domain_whois['domain']
            )
            event.execute()
        except peewee.OperationalError as e:
            print e
        except TableChoiceError as e:
            print e

    def insert_whois_info(self, **domain_whois):
        try:
            table_num = get_table_num(domain_whois['domain_hash'])
            event = self.model_list[table_num].insert(
                domain_hash=domain_whois['domain_hash'],
                domain=domain_whois['domain'],
                tld=domain_whois['domain'].split('.')[-1],
                flag=domain_whois['flag'],
                domain_status=domain_whois['domain_status'],
                sponsoring_registrar=domain_whois['sponsoring_registrar'],
                top_whois_server=domain_whois['top_whois_server'],
                sec_whois_server=domain_whois['sec_whois_server'],
                reg_name=domain_whois['reg_name'],
                reg_phone=domain_whois['reg_phone'],
                reg_email=domain_whois['reg_email'],
                org_name=domain_whois['org_name'],
                name_server=domain_whois['name_server'],
                creation_date=domain_whois['creation_date'],
                expiration_date=domain_whois['expiration_date'],
                updated_date=domain_whois['updated_date'],
                insert_time=domain_whois['insert_time'],
                details=domain_whois['details'],
                whois_hash=domain_whois['whois_hash']
            )
            event.execute()
        except peewee.OperationalError as e:
            print e
        except TableChoiceError as e:
            print e

    # 删除域名的whois信息
    def delete_whois_info(self, domain):
        try:
            domain_hash = hash(domain)
            table_num = get_table_num(domain_hash)
            event = self.model_list[table_num].delete().where(
                self.model_list[table_num].domain_hash == domain_hash,
                self.model_list[table_num].domain == domain
            )
            event.execute()
        except peewee.OperationalError as e:
            print e

    def set_whois_flag(self, domain, flag):
        try:
            domain_hash = hash(domain)
            table_num = get_table_num(domain_hash)
            event = self.model_list[table_num].update(
                flag=flag
            ).where(
                self.model_list[table_num].domain_hash == domain_hash,
                self.model_list[table_num].domain == domain
            )
            event.execute()
        except peewee.OperationalError as e:
            print e


class WhoisAddrDataBase:
    def __init__(self):
        self.whois_addr_model = model.whois_addr

    def connect(self):
        model.db_whois_addr.connect()

    def close(self):
        model.db_whois_addr.close()

    # 获取全部whois address 信息
    def query_all_whois_addr(self):
        try:
            query_results = self.whois_addr_model.select().where(
                self.whois_addr_model.addr is not None
            )
            return query_results
        except peewee.OperationalError as e:
            print e

    # 获取whois_server对应的tld
    def get_tld(self, whois_server):
        try:
            query_results = self.whois_addr_model.select(
                self.whois_addr_model.tld
            ).where(
                peewee.R('addr like %s', '%,' + whois_server) |
                peewee.R('addr like %s', whois_server + ',%') |
                peewee.R('addr = %s', whois_server),
                self.whois_addr_model.addr <> ''
            )
            return query_results
        except peewee.OperationalError as e:
            raise e

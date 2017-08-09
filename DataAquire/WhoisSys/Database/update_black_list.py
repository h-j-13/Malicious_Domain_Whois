#!/usr/bin/env python
# encoding:utf-8

"""
    定时更新相应数据到黑名单
======================

author    :   @`13
time      :   2017.5.24

数据标志位
NAME    -> 2
E-mail  -> 3
Tel     -> 4
"""

from db_opreation import DataBase
from Setting.static import Static

Static.static_value_init()


def update_black_list():
    """
    将反查数据更新到数据库中 
    """
    DB = DataBase()
    DB2 = DataBase()
    DB.db_connect()
    DB2.db_connect()
    DB.execute_no_return("""USE malicious_domain_sys""")
    DB2.execute_no_return("""USE malicious_domain_sys""")
    for results in DB.execute_Iterator("""SELECT info,info_type FROM info_reverse_search"""):
        for info, info_type in results:
            SQL = """INSERT IGNORE INTO reg_info_black_lists SET info = '{i}',type = {t},domain_count = -1""".format(
                i=info, t=info_type)
            DB2.execute_no_return(SQL)
        DB2.db_commit()
    DB2.db_commit()
    for results in DB.execute_Iterator("""SELECT info,type FROM reg_info_black_lists WHERE flag < 0"""):
        for info, type in results:
            if type == 2:
                reg_info_type = 'reg_name'
            elif type == 3:
                reg_info_type = 'reg_email'
            else:
                reg_info_type = 'reg_phone'
            SQL2 = """SELECT judge_flag,COUNT(*) FROM whois INNER JOIN domain_index ON whois.ID = domain_index.ID WHERE {info_type} = '{info}' GROUP BY judge_flag """.format(
                info_type=reg_info_type, info=info
            )
            domain_count = 0
            malicious_count = 0
            results_sql2 = DB2.execute(SQL2)
            if not results_sql2:
                continue
            for judge_flag, count in DB2.execute(SQL2):
                domain_count += count
                if judge_flag < 0:
                    malicious_count += count
            SQL3 = """UPDATE reg_info_black_lists SET domain_count = {d}, malicious_count={m}, flag = 1 WHERE info = '{info}'""".format(
                d=domain_count, m=malicious_count, info=info
            )
            print info
            DB2.execute_no_return(SQL3)
        DB2.db_commit()
    DB2.db_commit()
    DB.db_close()
    DB2.db_close()


if __name__ == '__main__':
    update_black_list()

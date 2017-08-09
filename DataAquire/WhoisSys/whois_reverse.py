#!/usr/bin/env python
# encoding:utf-8

"""
    whois数据反查更新
=======================

author    :   @`13
time      :   2017.05.07

数据标志位
NAME    -> 2
E-mail  -> 3
Tel     -> 4
"""

from Database.db_opreation import DataBase


def update_reverse_whois_info(sql):
    """更新需要反查的whois记录"""
    DB = DataBase()
    DB2 = DataBase()
    DB.db_connect()
    DB2.db_connect()
    DB2.execute("""USE malicious_domain_sys""")
    for result_list in DB.execute_Iterator(sql):
        for result in result_list:
            SQL_search_whois_info = """SELECT reg_name,reg_email,reg_phone FROM malicious_domain_sys.whois WHERE ID = {id}""".format(
                id=result[0])
            # print SQL_search_whois_info
            type_count = 2
            DATA = DB2.execute(SQL_search_whois_info)
            if DATA:
                for info in DATA[0]:
                    if info:
                        s = str(info)
                        SQL_insert_into_reverse_table = """INSERT IGNORE INTO info_reverse_search SET info = '{i}',info_type = '{t}' """.format(
                            i=s, t=type_count)
                        DB2.execute(SQL_insert_into_reverse_table)
                        # DB2.db_commit()
                    type_count += 1

    DB2.db_commit()
    DB.db_close()
    DB2.db_close()


if __name__ == '__main__':
    SQL_source_102 = """SELECT ID FROM malicious_domain_sys.domain_index WHERE source = 102"""
    SQL_judge_flag_2_or_3 = """SELECT ID FROM malicious_domain_sys.domain_index WHERE judge_flag = 2 OR judge_flag = 3"""

    update_reverse_whois_info(SQL_source_102)
    update_reverse_whois_info(SQL_judge_flag_2_or_3)

#!/usr/bin/env python
# encoding:utf-8

"""
    其他针对数据库的基础操作

author     :   @`13
version    :   0.1.0
last-update:   2017.3.25
"""


def input_domain(file, commitNum=200):
    """
    将域名导入数据库 
    """
    from db_opreation import DataBase
    from WhoisData.domain_analyse import DomainAnalyse
    DB = DataBase()
    DB.get_connect()
    DB.execute("""USE malicious_domain_sys""")
    f = open(file, 'r')
    count = 0
    for line in f.readlines():
        domain = line.split(' ')[0].strip()
        judge_flag = line.split(' ')[1].strip()
        D = DomainAnalyse(domain)
        print D.get_punycode_domain(),
        print judge_flag
        result = SQL = """INSERT INTO domain_index SET ID = {id}, domain = '{d}', judge_flag = {f} ;""".format(
            id=hash(D.get_punycode_domain().strip()), d=D.get_punycode_domain().strip(), f=judge_flag
        )
        if count >= commitNum:
            DB.db_commit()
            count = 0
            print D.get_punycode_domain().strip()
        DB.execute(SQL)
    f.close()
    DB.db_commit()
    DB.db_close()

if __name__ == '__main__':
    # Demo
    pass

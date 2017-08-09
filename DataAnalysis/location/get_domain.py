# -*- coding: utf-8 -*-
import re
import sys
import MySQLdb
from gen_SQL import SQL_generate#侯杰的数据库查找语句生成类
reload(sys)
sys.setdefaultencoding('utf-8')

class GetInfo(object):
    def __init__(self):
        self.connA = MySQLdb.connect(
            host='172.26.253.3',
            port=3306,
            user='root',
            passwd='platform'
        )
        self.connA.set_character_set('utf8')
        self.curA = self.connA.cursor()
        self.curA.execute("SET NAMES utf8")
        self.curA.execute("use malicious_domain_sys")
        self.connA.commit()

        self.c_reg_country = r'(?<=Registrant Country\:).*(?=\n)'
        self.c_reg_province = r'(?<=Registrant State/Province\:).*(?=\n)'
        self.c_reg_city = r'(?<=Registrant City\:).*(?=\n)'
        self.c_reg_postal = r'(?<=Registrant Postal Code\:).*(?=\n)'
        self.c_reg_street = r'((?<=Registrant Street\:)|(?<=Registrant Address1\:)).*(?=\n)'
        self.c_admin_country = r'(?<=Admin Country\:).*(?=\n)'
        self.c_admin_province = r'(?<=Admin State/Province\:).*(?=\n)'
        self.c_admin_city = r'(?<=Admin City\:).*(?=\n)'
        self.c_admin_postal = r'(?<=Admin Postal Code\:).*(?=\n)'
        self.c_tech_country = r'(?<=Tech Country\:).*(?=\n)'
        self.c_tech_province = r'(?<=Tech State/Province\:).*(?=\n)'
        self.c_tech_city = r'(?<=Tech City\:).*(?=\n)'
        self.c_tech_postal = r'(?<=Tech Postal Code\:).*(?=\n)'
        self.c_country = r'(?<=Country\:).*(?=\n)'
        self.c_province = r'(?<=State:).*(?=\n)'
        self.c_city = r'(?<=City\:).*(?=\n)'
        self.c_postal = r'(?<=Postal Code\:).*(?=\n)'
        self.c_street = r'(?<=(Street|Address1)\:).*(?=\n)'

        self.tables = []

    def get_detail_and_phone(self,domain):

        #str1 = SQL_generate.SELECT_by_domain(domain,'details')
        str1 = "SELECT details,reg_phone FROM whois WHERE ID = %d AND flag != -99" % hash(domain)
        count = self.curA.execute(str1)
        if count != 0:
            detail,phone = self.curA.fetchone()

            return detail, phone
        else:
            return None


    def get_info_from_detail(self,domain,detail):

        reg_country = None
        reg_province = None
        reg_street = None
        reg_city = None
        reg_postal = None

        if detail:
            try:
                reg_country = re.search(self.c_reg_country, detail).group().strip()
            except:
                try:
                    reg_country = re.search(self.c_country, detail).group().strip()
                except:
                    reg_country = None
            if reg_country:
                try:
                    reg_province = re.search(self.c_reg_province, detail).group().strip()
                except:
                    try:
                        reg_province = re.search(self.c_province, detail).group().strip()
                    except:
                        reg_province = None
                try:
                    reg_street = re.search(self.c_reg_street, detail).group().strip()
                except:
                    try:
                        reg_street = re.search(self.c_street, detail).group().strip()
                    except:
                        reg_street = None
                try:
                    reg_city = re.search(self.c_reg_city, detail).group().strip()
                except:
                    try:
                        reg_city = re.search(self.c_city, detail).group().strip()
                    except:
                        reg_city = None
                try:
                    reg_postal = re.search(self.c_reg_postal, detail).group().strip()
                except:
                    try:
                        reg_postal = re.search(self.c_postal, detail).group().strip()
                    except:
                        reg_postal = None
            else:
                reg_province = None
                reg_street = None
                reg_city = None
                reg_postal = None

            '''
            #为非空结果加上引号
            if reg_street != "null":
                reg_street = "'" + MySQLdb.escape_string(reg_street) + "'"
            if reg_province != "null":
                reg_province = "'" + MySQLdb.escape_string(reg_province) + "'"
            if reg_city != "null":
                reg_city = "'" + MySQLdb.escape_string(reg_city) + "'"
            if reg_postal != "null":
                reg_postal = "'" + MySQLdb.escape_string(reg_postal) + "'"
            
            try:
                curA.execute('UPDATE whois SET country="%s",province=%s,city=%s,postal_code=%s,street=%s WHERE domain = "%s"' % (reg_country,reg_province,reg_city,reg_postal,reg_street,domain))
                ccc += 1
                connA.commit()
            except:
                print 'UPDATE whois SET country="%s",province=%s,city=%s,postal_code=%s,street=%s WHERE domain = "%s"' % (MySQLdb.escape_string(reg_country),MySQLdb.escape_string(reg_province.lower()),MySQLdb.escape_string(reg_city.lower()),MySQLdb.escape_string(reg_postal),MySQLdb.escape_string(reg_street),MySQLdb.escape_string(domain))
            '''
        return {'domain':domain, 'reg_country':reg_country,'reg_province':reg_province, 'reg_city':reg_city, 'reg_postal':reg_postal, 'reg_street':reg_street}

        





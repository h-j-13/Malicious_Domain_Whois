#coding=utf-8
import sys
import MySQLdb
from get_domain import GetInfo
from whois2addr import Whois2Addr
from postal2addr import Postal2Addr
from single_phone import Phone

reload(sys)
sys.setdefaultencoding('utf-8')

class DomainAddr(object):
    def __init__(self):
        self.conn = MySQLdb.connect(
            host='172.26.253.3',
            port=3306,
            user='root',
            passwd='platform'
        )
        self.conn.set_character_set('utf8')
        self.cur = self.conn.cursor()
        self.cur.execute("SET NAMES utf8")
        self.cur.execute("use malicious_domain_sys;")

        self.domains = []

        self.getinfo = GetInfo()
        self.w2a = Whois2Addr()
        self.p2a = Postal2Addr()
        self.t2a = Phone()

    def run(self):
        c_ok = 0
        c_bad = 0
        sqlstr = "SELECT domain FROM domain_index WHERE whois_flag != -99 AND locate_flag = -10"
        count = self.cur.execute(sqlstr)
        if count == 0:
            print '[ERROR]:Get no domain'
            exit()
        print count
        self.domains = list(self.cur.fetchall())
        for d in self.domains:
            flag = 0
            domain = d[0]
            uuid = hash(domain)
            detail,phone = self.getinfo.get_detail_and_phone(domain)
            #print detail
            if detail:
                reg_detail = self.getinfo.get_info_from_detail(domain,detail)
                reg_detail['reg_phone'] = phone
                #print reg_detail
                if reg_detail['reg_country']:
                    reg_phone_detail = self.t2a.analysis(reg_detail['reg_phone'])
                    if reg_detail['reg_country'].lower() == 'china' or reg_detail['reg_country'].lower() == 'cn':
                        reg_city_detail = self.w2a.analyze(reg_detail['reg_province'],reg_detail['reg_city'])
                        reg_postal_detail = self.p2a.analyze(reg_detail['reg_postal'])
                    else:
                        reg_city_detail = (None, None, None)#province, city, flag
                        reg_postal_detail = (None, None, None)
                else:
                    reg_city_detail = (None, None, None)
                    reg_postal_detail = (None, None, None)
                    reg_phone_detail = (None, None, None)  # country, province, city
                sqlstr = "INSERT INTO locate SET "#(ID, country, province, city, postal_code, street, reg_whois_province, reg_whois_city, reg_postal_province, reg_postal_city, flag) VALUES ("
                sqlstr += "id = %d," % uuid
                sqlstr += "country = %s," % genstr(reg_detail['reg_country'])
                sqlstr += "province = %s," % genstr(reg_detail['reg_province'])
                sqlstr += "city = %s," % genstr(reg_detail['reg_city'])
                sqlstr += "postal_code = %s," % genstr(reg_detail['reg_postal'])
                sqlstr += "street = %s," % genstr(reg_detail['reg_street'])
                sqlstr += "phone = %s," % genstr(reg_detail['reg_phone'])
                sqlstr += "reg_whois_province = %s," % genstr(reg_city_detail[0])
                sqlstr += "reg_whois_city = %s," % genstr(reg_city_detail[1])
                sqlstr += "reg_phone_province = %s," % genstr(reg_phone_detail[1])
                sqlstr += "reg_phone_city = %s," % genstr(reg_phone_detail[2])
                sqlstr += "reg_postal_province = %s," % genstr(reg_postal_detail[0])
                sqlstr += "reg_postal_city = %s," % genstr(reg_postal_detail[1])
                sqlstr += "reg_postal_county = %s," % genstr(reg_postal_detail[2])
                if reg_phone_detail[0]:
                    if reg_phone_detail[0] == '中国':
                        flag += 10000
                    else:
                        flag += 20000
                else:
                    flag += 30000
                if reg_city_detail[0]:
                    if reg_city_detail[1]:
                        flag += 1000
                    else:
                        flag += 2000
                else:
                    flag += 3000
                if reg_postal_detail[0]:
                    if reg_postal_detail[1]:
                        if reg_postal_detail[2][:2]!= 'NO':
                            flag += 100
                        elif reg_postal_detail[2][-1:] == '1':
                            flag += 200
                        else:
                            flag += 300
                else:
                    flag += 400
                sqlstr += "flag = %d" % flag
                self.cur.execute(sqlstr)
                self.conn.commit()
                c_ok +=1
            else:
                sqlstr = "INSERT INTO locate SET "
                sqlstr += "id = %d," % uuid
                sqlstr += "flag = %d" % 0
                self.cur.execute(sqlstr)
                self.conn.commit()
                c_bad += 1
        print 'ok=',c_ok,'  bad=',c_bad



def genstr(str1):
    if str1:
        return "'" + MySQLdb.escape_string(str1) + "'"
    else:
        return "''"

if __name__ == '__main__':
    da = DomainAddr()
    da.run()

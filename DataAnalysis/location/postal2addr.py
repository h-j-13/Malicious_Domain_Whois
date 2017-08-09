#coding=utf-8
'''
解析whois信息中邮编的地理位置
'''
import sys
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf-8')

class Postal2Addr(object):

    def __init__(self):
        #连接数据库
        self.connA = MySQLdb.connect(	
                host ='172.26.253.3',
                port = 3306,
                user ='root',
                passwd ='platform'
            )
        self.connA.set_character_set('utf8')
        self.curA = self.connA.cursor()
        self.curA.execute("SET NAMES utf8")
        self.curA.execute("use zgx;")

        self.p_ect0 = [["市", ""], ["省", ""], ["特别行政区", ""], ["维吾尔自治区", ""], ["壮族自治区", ""], ["宁夏回族自治区", ""], ["藏族自治州",""], ["自治区", ""]]
        self.p_ect1 = [["市", ""], ["地区", ""], ["区", ""], ["县", ""], ["土家族苗族自治州", ""], ["回族自治州", ""], ["蒙古自治州", ""], ["哈萨克自治州", ""], ["柯尔克孜自治州", ""], ["自治州", ""]]

    def change(self,data_t):
        if data_t:
            data = list(data_t)
            for ect in self.p_ect0:
                if ect[0] in data[0]:
                    data[0] = data[0].replace(ect[0],ect[1])
                    break
            if "辖区" in data[1]:
                data[1] = data[0]
            else:
                for ect in self.p_ect1:
                    if ect[0] in data[1][-len(ect[0]):]:
                        data[1] = data[1].replace(ect[0],ect[1])
                        break
            return data
        else:
            return None, None, None

    def analyze(self,postal):
        if postal is None:
            return None,None,None

        if len(postal) == 6:
            #匹配数据库中的邮编
            try:
                self.curA.execute('select * from zip_code1 WHERE code = "%s" LIMIT 1' % (postal)  )
                data = self.curA.fetchone()
            except:
                data = None
            if data and data != 'NULL':
                detail = (data[1], data[2], data[3])
            else:
                #缩减一位
                try:
                    self.curA.execute('select * from zip_code1 WHERE code regexp "%s." LIMIT 1' % (postal[:5])  )
                    data = self.curA.fetchone()
                except:
                    data = None
                if data and data != 'NULL':
                    detail = (data[1], data[2], 'NO1')
                else:
                    #缩减两位
                    try:
                        self.curA.execute('select * from zip_code1 WHERE code regexp "%s.." LIMIT 1' % (postal[:4])  )
                        data = self.curA.fetchone()
                    except:
                        data = None
                    if data and data != 'NULL':
                        detail =  (data[1], data[2], 'NO2')
                    else:
                        detail = None
        else:
            detail = None
        return self.change(detail)
        #str = 'UPDATE whois_zgx_temp SET reg_postal_detail = "%s" WHERE domain = "%s"' % (detail,domain)
    

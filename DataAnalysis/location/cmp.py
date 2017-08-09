#coding=utf-8
import sys
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')

class CMP(object):
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


    def select(self, id):
        sqlstr = "SELECT ID, country, reg_whois_province, reg_whois_city, reg_postal_province, reg_postal_city, ICP_province, IP_info, reg_phone_province, reg_phone_city FROM locate WHERE ID = %d" % id
        count = self.cur.execute(sqlstr)
        if count != 0:
            result = self.cur.fetchone()
            country = result[1]
            if country.lower() in ('china','cn'):
                ip_info = result[7]
                ip_list = []
                ip_t =ip_info.split(',')
                for t in ip_t:
                    if t != '':
                        tt=t.split('|')
                        ip_list.append([tt[2],tt[3]])

            else:
                return -2   #非中国
            return [[result[2],result[3]], [result[4],result[5]], ip_list, result[6], [result[8],result[9]]]
        else:
            return -1

    def compare(self, lst):
        #print lst
        province = ['']
        city = ['']
        flagp = [0,0,0,0,0,0]#相同数量，电话，whois，邮编，
        flagc = [0,0,0,0,0]



        #whois
        s = False
        for index,p in enumerate(province):
            if p == lst[0][0]:
                s = True
                flagp[2] = index
                break
        if not s:
            province.append(lst[0][0])
            flagp[2] = len(province)-1

        s = False
        for index, c in enumerate(city):
            if c == lst[0][1]:
                s = True
                flagc[2] = index
                break
        if not s:
            city.append(lst[0][1])
            flagc[2] = len(city) - 1

        #postal
        s = False
        for index, p in enumerate(province):
            if p == lst[1][0]:
                s = True
                flagp[3] = index
                break
        if not s:
            province.append(lst[1][0])
            flagp[3] = len(province) - 1

        s = False
        for index, c in enumerate(city):
            if c == lst[1][1]:
                s = True
                flagc[3] = index
                break
        if not s:
            city.append(lst[1][1])
            flagc[3] = len(city) - 1

        #icp
        s = False
        for index, p in enumerate(province):
            if p == lst[3]:
                s = True
                flagp[5] = index
                break
        if not s:
            province.append(lst[3])
            flagp[5] = len(province) - 1

        #ip
        s = False
        for l in lst[2]:
            #print l
            for index, p in enumerate(province[1:]):
                if p in l[0]:
                    s = True
                    flagp[4] = index+1
                    break
        if not s:
            flagp[4] = 0

        s = False
        for l in lst[2]:
            #print l
            for index, c in enumerate(city[1:]):
                if c in l[1]:
                    s = True
                    flagc[4] = index+1
                    break
        if not s:
            flagc[4] = 0

        #phone
        s = False
        for index, p in enumerate(province[1:]):
            #print lst[4][0]
            if p in lst[4][0]:
                s = True
                flagp[1] = index+1
                break
        if not s:
            province.append(lst[4][0])
            flagp[1] = len(province) - 1

        s = False
        for index, c in enumerate(city[1:]):
            if c in lst[4][1]:
                s = True
                flagc[1] = index+1
                break
        if not s:
            city.append(lst[4][1])
            flagc[1] = len(city) - 1



        #find most
        mostp=self.most_common(flagp)
        if mostp == 0:
            flagp[0] = 0
        else:
            flagp[0]=flagp[1:].count(mostp)
            for p in range(1,len(flagp)):
                if flagp[p] == 1:
                    flagp[p] = mostp
                elif flagp[p] == mostp:
                    flagp[p] = 1

        mostc = self.most_common(flagc)
        if mostc == 0:
            flagc[0] = 0
        else:
            flagc[0] = flagc[1:].count(mostc)
            for c in range(1,len(flagc)):
                if flagc[c] == 1:
                    flagc[c] = mostc
                elif flagc[c] == mostc:
                    flagc[c] = 1

        iflagp = 0
        iflagc = 0
        for p in flagp:
            iflagp = iflagp * 10 + p
        for c in flagc:
            iflagc = iflagc * 10 + c


        return iflagp,iflagc

    def most_common(self,seq):
        d = {}
        for i in seq:
            if i == 0:
                continue
            d[i] = d.get(i, 0) + 1
        if d == {}:
            return 0
        ret = []
        for j in sorted(d.items(), reverse=True, key=lambda x:x[1]):
            if len(ret) == 0:
                ret.append(j[0])
                n = j[1]
            else:
                if j[1] == n:
                    ret.append(j[0])
                else:
                    break
        return ret[0]

    def __del__(self):
        self.cur.close()
        self.conn.close()

if __name__ == '__main__':

    conn = MySQLdb.connect(
        host='172.26.253.3',
        port=3306,
        user='root',
        passwd='platform'
    )
    conn.set_character_set('utf8')
    cur = conn.cursor()
    cur.execute("SET NAMES utf8")
    cur.execute("use malicious_domain_sys;")

    cmp = CMP()
    count = cur.execute("SELECT ID FROM locate WHERE flag>0 #and cmp=0")
    print count
    if count != 0:
        idlist = cur.fetchall()
        for i in idlist:
            id = i[0]
            info = cmp.select(id)
            #print id,
            if type(info) is int:
                result = info
                sqlstr = "UPDATE locate SET cmp=%d WHERE ID = %d" % (result, id)
                #cur.execute(sqlstr)
                print result
            else:
                result = cmp.compare(info)
                sqlstr = "UPDATE locate SET cmp = %d%d, cmpinfo='%06d%05d' WHERE ID = %d" % (result[0]/100000,result[1]/10000,result[0],result[1],id)
                #cur.execute(sqlstr)
                print '%06d, %05d' % (result[0],result[1])
            #conn.commit()
            #insert
    cur.close()
    conn.close()


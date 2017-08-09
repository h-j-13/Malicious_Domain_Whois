#coding=utf-8
'''
格式化不同数据库带来的地理位置格式不同问题,并简略对比
'''


import re
import sys
import MySQLdb
import datetime
    

#pcmpw标志意义：    3：数据库获取数据错误     0:省不同    1：市不同    10：省市相同


reload(sys)
sys.setdefaultencoding('utf-8')
    
p_ect0 = [["市", ""], ["省", ""], ["特别行政区", ""], ["维吾尔自治区", ""], ["壮族自治区", ""], ["宁夏回族自治区", ""], ["藏族自治州",""], ["自治区", ""]]
p_ect1 = [["市", ""], ["地区", ""], ["区", ""], ["县", ""], ["土家族苗族自治州", ""], ["回族自治州", ""], ["蒙古自治州", ""], ["哈萨克自治州", ""], ["柯尔克孜自治州", ""], ["自治州", ""]]

def change(data):
    for ect in p_ect0:
        if ect[0] in data[0]:
            data[0] = data[0].replace(ect[0],ect[1])
            break
    if "辖区" in data[1]:
        data[1] = data[0]
    else:
        for ect in p_ect1:
            if ect[0] in data[1][-len(ect[0]):]:
                data[1] = data[1].replace(ect[0],ect[1])
                break
    return data
                

if __name__ == "__main__":
    start = datetime.datetime.now()
    conn = MySQLdb.connect(	
        host ='172.29.152.249',
        port = 3306,
        user ='root',
        passwd ='platform'
    )
    conn.set_character_set('utf8')
    cur = conn.cursor()
    cur.execute("SET NAMES utf8")
    cur.execute("use xj_domain_monitoring;")
    conn.commit()
    
    count = cur.execute('select domain,reg_postal_detail,reg_city_detail,reg_postal from whois_zgx_temp WHERE cmp is null (reg_province is not null OR reg_city is not null OR reg_postal is not null) ') #LIMIT
    result = cur.fetchall()
    cc = 0
    per = 0.0
    s_per = 0.0
    print "     邮编 Whois"
    for r in result:
        pcmpw = 10
        try:
            if r[1] is None:
                p_data = ['NULL']
            else:
                p_data = r[1].split("_")
            if r[2] is None:
                c_data = ['NULL']
            else:
                c_data = r[2].split("_")
        except:
            print "ERROR1:",r
            pcmpw = 3
            cur.execute('UPDATE whois_zgx_temp SET cmp = %d WHERE domain = "%s"' % (pcmpw, r[0]))
            loop += 1
            continue
        if p_data[0] == "NULL" and len(p_data) == 1:
            p_data.append("NULL")
            p_data.append("NULL")
        if c_data[0] == "NULL" and len(c_data) == 1:
            c_data.append("NULL")
        if 1==1:
            if len(p_data) != 3 or len(c_data) < 2:
                print "ERROR2:",r
                pcmpw = 3
                cur.execute('UPDATE whois_zgx_temp SET cmp = %d WHERE domain = "%s"' % (pcmpw, r[0]))
                continue
            else:
                p_data = change(p_data)
                '''
                for i in p_data:
                    print i,
                print ""
                '''
                if p_data[0] in "北京上海重庆天津":
                    if c_data[0] in "北京上海重庆天津":
                        p_data[1] = c_data[1]
                        #print "1111111",p_data[1], c_data[1]
                else:
                    if ((p_data[0] != c_data[0]) or (c_data[0] == "NULL") or (p_data[0] == "NULL")):
                        #print "0:  ",p_data[0],c_data[0],r[3],'"',r[0],'"'
                        pcmpw = 0
                    if ((p_data[1] != c_data[1]) or (c_data[1] == "NULL") or (p_data[1] == "NULL")):
                        #print "1:  ",p_data[1],c_data[1],r[3],p_data[2],'"',r[0],'"'
                        pcmpw = 1
                    #else:
                        #print p_data[1],c_data[1]
    
    
        
        cur.execute('UPDATE whois_zgx_temp SET reg_postal_province = "%s", reg_postal_city = "%s", reg_postal_county = "%s", reg_whois_province = "%s", reg_whois_city = "%s", cmp = %d WHERE domain = "%s"' % (p_data[0], p_data[1], p_data[2], c_data[0], c_data[1] ,pcmpw, r[0]))
        cc += 1
        per = float(cc)/float(count)
        #print per,count,cok,cbad
        if per - s_per > 0.01:
            s_per = per
            print '%.1f%%' % (s_per*100)
    conn.commit()
    end = datetime.datetime.now()
    print "time: %f s" % (end - start).seconds

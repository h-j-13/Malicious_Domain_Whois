# coding=utf-8
"""
功能：从数据库icp信息中得到省份及简称
作者:郑乐斌
更新时间:2016.8.20
"""

import MySQLdb
import sys


reload(sys)
# python默认编码是Ascii
sys.setdefaultencoding("utf-8")

def get_province():

    # address = ['京','津','冀','晋','蒙','辽','吉','黑','沪','苏','浙','皖',
    #            '闽','赣','鲁','豫','鄂','湘','粤','桂','琼','渝','川','贵',
    #            '云','藏','陕','甘','青','新','蜀','滇','陇','黔']

    address = {'京':'北京','津':'天津','冀':'河北','晋':'山西','蒙':'内蒙古','辽':'辽宁','吉':'吉林',
               '黑':'黑龙江','沪':'上海','苏':'江苏','浙':'浙江','皖':'安徽','黔':'贵州','宁':'宁夏',
               '闽':'福建','赣':'江西','鲁':'山东','豫':'河南','鄂':'湖北','湘':'湖南','粤':'广东',
               '桂':'广西','琼':'海南','渝':'重庆','川':'四川','贵':'贵州','滇':'云南','陇':'甘肃',
               '云':'云南','藏':'西藏','陕':'陕西','甘':'甘肃','青':'青海','新':'新疆','蜀':'四川',
               '淅':'浙江','卾':'湖北','港':'香港'}


    flag = 0
    icps = []
    try:
        db = MySQLdb.connect(host='172.26.253.3', 
                            user='root', 
                            passwd='platform', 
                            charset = "utf8",
                            db='zgx'
                            )
        cur = db.cursor()
        sql = "SELECT domain, icp FROM domains WHERE flag = 3"
        sql2 = "UPDATE domains SET simple_name = %s, ICP_province = %s WHERE domain = %s"
        sql3 = "UPDATE domains SET flag = %s WHERE domain = %s"

        count = cur.execute(sql)
        icps = cur.fetchall()

        for icp in icps:
            # print icp[-1].encode('utf-8')
            for add in address.keys():
                if add in str(icp[-1]).encode('utf-8'):
                    print add
                    # print icp[0]
                    count = cur.execute(sql2, (add, address[add], icp[0]))
                    db.commit()
        
        db.close()
        print len(icps)

    except Exception, e:
        raise e


def get_domain_distribution():

    # address = ['京','津','冀','晋','蒙','辽','吉','黑','沪','苏','浙','皖',
    #            '闽','赣','鲁','豫','鄂','湘','粤','桂','琼','渝','川','贵',
    #            '云','藏','陕','甘','青','新','蜀','滇','陇','黔']

    address = {'北京':0,'天津':0,'河北':0,'山西':0,'内蒙古':0,'辽宁':0,'吉林':0,
               '黑龙江':0,'上海':0,'江苏':0,'浙江':0,'安徽':0,'贵州':0,'宁夏':0,
               '福建':0,'江西':0,'山东':0,'河南':0,'湖北':0,'湖南':0,'广东':0,
               '广西':0,'海南':0,'重庆':0,'四川':0,'云南':0,'甘肃':0,
               '西藏':0,'陕西':0,'青海':0,'新疆':0, '香港':0, '澳门':0}


    flag = 0
    icps = []
    try:
        db = MySQLdb.connect(host='172.26.253.3', 
                            user='root', 
                            passwd='platform', 
                            charset = "utf8",
                            db='zgx'
                            )
        cur = db.cursor()
        sql = "SELECT domain, ICP_province FROM domains WHERE flag = 1 AND ICP_province IS NOT NULL"

        count = cur.execute(sql)
        ICP_province = cur.fetchall()

        for domain in ICP_province:
            # print domain[-1]
            for province in address.keys():
                if province == str(domain[-1]).encode('utf-8'):
                    address[province] += 1;
                    if str(domain[-1]).encode('utf-8') == 'None':
                        print domain[0] + ':' + str(domain[-1]).encode('utf-8')

        
        sql1 = "INSERT INTO domain_distribution(province, number, source) VALUES (%s, %s, %s)"
        print len(ICP_province)
        for value in address:
            print value + ':' + str(address[value])
            count = cur.execute(sql1, (value, address[value], 'ICP'))
            db.commit()

        db.close()

    except Exception, e:
        raise e

def get_domains():

    flag = 0
    icps = []
    try:
        db = MySQLdb.connect(host='172.26.253.3', 
                            user='root', 
                            passwd='platform', 
                            charset = "utf8",
                            db='WK'
                            )
        cur = db.cursor()
        sql = "SELECT domain FROM domains_swkong"
        # sql2 = "UPDATE domains SET simple_name = %s, ICP_province = %s WHERE domain = %s"
        # sql3 = "UPDATE domains SET flag = %s WHERE domain = %s"

        count = cur.execute(sql)
        icps = cur.fetchall()
        db.close()

        db = MySQLdb.connect(host='172.26.253.3', 
                            user='root', 
                            passwd='platform', 
                            charset = "utf8",
                            db='zlb'
                            )
        cur = db.cursor()
        sql = "INSERT INTO domain(domain, flag) VALUES (%s, %s)"
        # sql2 = "UPDATE domains SET simple_name = %s, ICP_province = %s WHERE domain = %s"
        # sql3 = "UPDATE domains SET flag = %s WHERE domain = %s"

        # count = cur.execute(sql)
        # icps = cur.fetchall()
        for icp in icps:
            count = cur.execute(sql, (icp, 0))
            db.commit()
            print str(icp) + " OK !!"
        
        db.close()
        print len(icps)

    except Exception, e:
        raise e

if __name__ == '__main__':

    get_domain_distribution()
    # get_province()
    # get_domains()



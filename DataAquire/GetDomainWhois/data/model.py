# /usr/bin/python
# encoding:utf-8

import peewee
import ConfigParser
cf = ConfigParser.ConfigParser()
cf.read("data.conf")

# whois 数据表
db_whois = peewee.MySQLDatabase(
    host=cf.get('DataBase', 'host'),
    user=cf.get('DataBase', 'user'),
    passwd=cf.get('DataBase', 'passwd'),
    database=cf.get('DataBase', 'whoisDataBase'),
    charset=cf.get('DataBase', 'charset'),
    port=cf.getint('DataBase', 'port')
)

# whois 服务数据表
db_whois_addr = peewee.MySQLDatabase(
    host=cf.get('DataBase', 'host'),
    user=cf.get('DataBase', 'user'),
    passwd=cf.get('DataBase', 'passwd'),
    database=cf.get('DataBase', 'whoisAddrBase'),
    charset=cf.get('DataBase', 'charset'),
    port=cf.getint('DataBase', 'port')
)


class WhoisBaseModel(peewee.Model):
    id = peewee.IntegerField()   # 表内信息字段
    domain_hash = peewee.BigIntegerField()
    domain = peewee.CharField()
    tld = peewee.CharField()
    flag = peewee.IntegerField()
    domain_status = peewee.CharField()
    sponsoring_registrar = peewee.CharField()
    top_whois_server = peewee.CharField()
    sec_whois_server = peewee.CharField()
    reg_name = peewee.CharField()
    reg_phone = peewee.CharField()
    reg_email = peewee.CharField()
    org_name = peewee.CharField()
    name_server = peewee.CharField()
    creation_date = peewee.CharField()
    expiration_date = peewee.CharField()
    updated_date = peewee.CharField()
    insert_time = peewee.DateTimeField()
    details = peewee.TextField()
    whois_hash = peewee.BigIntegerField()

    class Meta():
        database = db_whois

class domain_whois_1(WhoisBaseModel):pass
class domain_whois_2(WhoisBaseModel):pass
class domain_whois_3(WhoisBaseModel):pass
class domain_whois_4(WhoisBaseModel):pass
class domain_whois_5(WhoisBaseModel):pass
class domain_whois_6(WhoisBaseModel):pass
class domain_whois_7(WhoisBaseModel):pass
class domain_whois_8(WhoisBaseModel):pass
class domain_whois_9(WhoisBaseModel):pass
class domain_whois_10(WhoisBaseModel):pass
class domain_whois_11(WhoisBaseModel):pass
class domain_whois_12(WhoisBaseModel):pass
class domain_whois_13(WhoisBaseModel):pass
class domain_whois_14(WhoisBaseModel):pass
class domain_whois_15(WhoisBaseModel):pass
class domain_whois_16(WhoisBaseModel):pass
class domain_whois_17(WhoisBaseModel):pass
class domain_whois_18(WhoisBaseModel):pass
class domain_whois_19(WhoisBaseModel):pass
class domain_whois_20(WhoisBaseModel):pass
class domain_whois_21(WhoisBaseModel):pass
class domain_whois_22(WhoisBaseModel):pass
class domain_whois_23(WhoisBaseModel):pass
class domain_whois_24(WhoisBaseModel):pass
class domain_whois_25(WhoisBaseModel):pass
class domain_whois_26(WhoisBaseModel):pass
class domain_whois_27(WhoisBaseModel):pass
class domain_whois_28(WhoisBaseModel):pass
class domain_whois_29(WhoisBaseModel):pass
class domain_whois_30(WhoisBaseModel):pass
class domain_whois_31(WhoisBaseModel):pass
class domain_whois_32(WhoisBaseModel):pass
class domain_whois_33(WhoisBaseModel):pass
class domain_whois_34(WhoisBaseModel):pass
class domain_whois_35(WhoisBaseModel):pass
class domain_whois_36(WhoisBaseModel):pass
class domain_whois_37(WhoisBaseModel):pass
class domain_whois_38(WhoisBaseModel):pass
class domain_whois_39(WhoisBaseModel):pass
class domain_whois_40(WhoisBaseModel):pass
class domain_whois_41(WhoisBaseModel):pass
class domain_whois_42(WhoisBaseModel):pass
class domain_whois_43(WhoisBaseModel):pass
class domain_whois_44(WhoisBaseModel):pass
class domain_whois_45(WhoisBaseModel):pass
class domain_whois_46(WhoisBaseModel):pass
class domain_whois_47(WhoisBaseModel):pass
class domain_whois_48(WhoisBaseModel):pass
class domain_whois_49(WhoisBaseModel):pass
class domain_whois_50(WhoisBaseModel):pass
class domain_whois_51(WhoisBaseModel):pass
class domain_whois_52(WhoisBaseModel):pass
class domain_whois_53(WhoisBaseModel):pass
class domain_whois_54(WhoisBaseModel):pass
class domain_whois_55(WhoisBaseModel):pass
class domain_whois_56(WhoisBaseModel):pass
class domain_whois_57(WhoisBaseModel):pass
class domain_whois_58(WhoisBaseModel):pass
class domain_whois_59(WhoisBaseModel):pass
class domain_whois_60(WhoisBaseModel):pass
class domain_whois_61(WhoisBaseModel):pass
class domain_whois_62(WhoisBaseModel):pass
class domain_whois_63(WhoisBaseModel):pass
class domain_whois_64(WhoisBaseModel):pass
class domain_whois_65(WhoisBaseModel):pass
class domain_whois_66(WhoisBaseModel):pass
class domain_whois_67(WhoisBaseModel):pass
class domain_whois_68(WhoisBaseModel):pass
class domain_whois_69(WhoisBaseModel):pass
class domain_whois_70(WhoisBaseModel):pass
class domain_whois_71(WhoisBaseModel):pass
class domain_whois_72(WhoisBaseModel):pass
class domain_whois_73(WhoisBaseModel):pass
class domain_whois_74(WhoisBaseModel):pass
class domain_whois_75(WhoisBaseModel):pass
class domain_whois_76(WhoisBaseModel):pass
class domain_whois_77(WhoisBaseModel):pass
class domain_whois_78(WhoisBaseModel):pass
class domain_whois_79(WhoisBaseModel):pass
class domain_whois_80(WhoisBaseModel):pass
class domain_whois_81(WhoisBaseModel):pass
class domain_whois_82(WhoisBaseModel):pass
class domain_whois_83(WhoisBaseModel):pass
class domain_whois_84(WhoisBaseModel):pass
class domain_whois_85(WhoisBaseModel):pass
class domain_whois_86(WhoisBaseModel):pass
class domain_whois_87(WhoisBaseModel):pass
class domain_whois_88(WhoisBaseModel):pass
class domain_whois_89(WhoisBaseModel):pass
class domain_whois_90(WhoisBaseModel):pass
class domain_whois_91(WhoisBaseModel):pass
class domain_whois_92(WhoisBaseModel):pass
class domain_whois_93(WhoisBaseModel):pass
class domain_whois_94(WhoisBaseModel):pass
class domain_whois_95(WhoisBaseModel):pass
class domain_whois_96(WhoisBaseModel):pass
class domain_whois_97(WhoisBaseModel):pass
class domain_whois_98(WhoisBaseModel):pass
class domain_whois_99(WhoisBaseModel):pass
class domain_whois_100(WhoisBaseModel):pass


class whois_addr(peewee.Model):
    tld = peewee.CharField()  # 顶级域名
    addr = peewee.CharField()  # 顶级域名对应的whois服务器

    class Meta():
        database = db_whois_addr

if __name__ == '__main__':
    cf = ConfigParser.ConfigParser()
    cf.read("data.conf")
    print cf.get('DataBase', 'host')


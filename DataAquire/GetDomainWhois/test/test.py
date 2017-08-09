# !usr/bin/python
# encoding:utf8



import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import peewee
from domain_analyse import  DomainAnalyse

db_whois = peewee.MySQLDatabase(host='172.29.152.249',
        user='root',
        passwd='platform',
        database='domain_whois',
        charset='utf8',
        port=3306)

class WhoisBaseModel(peewee.Model):
    id = peewee.IntegerField()
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

class domain_whois_1(WhoisBaseModel): pass


db_whois_addr = peewee.MySQLDatabase(host='172.26.253.3',
        user='root',
        passwd='platform',
        database='domain_whois',
        charset='utf8',
        port=3306)

class whois_addr(peewee.Model):
    addr = peewee.CharField()
    tld = peewee.CharField()
    class Meta():
        database = db_whois_addr



if __name__ == '__main__':
    str = """whois.verisign-grs.com : com_manage
whois.crsnic.net : com_manage
whois.cnnic.cn : cn_manage
whois.cnnic.net.cn : cn_manage
whois.donuts.co : general_manage
whois.afilias-srs.net : general_manage
whois-dub.mm-registry.com : general_manage
capetown-whois.registry.net.za : general_manage
whois-alsace.nic.fr : general_manage
whois-ovh.nic.fr : general_manage
whois-paris.nic.fr : general_manage
whois.afilias.net : general_manage
whois.aridnrs.net.au : general_manage
whois.cmc.iq : general_manage
whois.donuts.co : general_manage
whois.eus.coreregistry.net : general_manage
whois.gal.coreregistry.net : general_manage
whois.gtld.knet.cn : general_manage
whois.kenic.or.ke : general_manage
whois.ksregistry.net : general_manage
whois.kyregistry.ky : general_manage
whois.na-nic.com.na : general_manage
whois.ngtld.cn : general_manage
whois.nic.af : general_manage
whois.nic.berlin : general_manage
whois.nic.bj : general_manage
whois.nic.brussels : general_manage
whois.nic.career : general_manage
whois.nic.cx : general_manage
whois.nic.cymru : general_manage
whois.nic.frl : general_manage
whois.nic.gent : general_manage
whois.nic.gl : general_manage
whois.nic.global : general_manage
whois.nic.gmo : general_manage
whois.nic.gs : general_manage
whois.nic.hamburg : general_manage
whois.nic.ht : general_manage
whois.nic.ki : general_manage
whois.nic.kiwi : general_manage
whois.nic.luxury : general_manage
whois.nic.menu : general_manage
whois.nic.mg : general_manage
whois.nic.moscow : general_manage
whois.nic.ms : general_manage
whois.nic.mu : general_manage
whois.nic.mz : general_manage
whois.nic.net.ng :general_manage
whois.nic.net.sb : general_manage
whois.nic.nf : general_manage
whois.nic.ooo : general_manage
whois.nic.quebec : general_manage
whois.nic.reise : general_manage
whois.nic.sydney : general_manage
whois.nic.tc : general_manage
whois.nic.tl : general_manage
whois.nic.top : general_manage
whois.nic.trust : general_manage
whois.nic.wales : general_manage
whois.nic.wien : general_manage
whois.nic.xn--80adxhks : general_manage
whois.nic.xxx : general_manage
whois.pandi.or.id : general_manage
whois.pir.org : general_manage
whois.publicinterestregistry.net : general_manage
whois.registre.ma : general_manage
whois.registry.gy : general_manage
whois.rightside.co : general_manage
whois.sx : general_manage
whois.tld.sy : general_manage
whois.uniregistry.net : general_manage
whois.unitedtld.com : general_manage
whois1.nic.bi : general_manage
whois.nic.ac : ac_manage
whois.aero : general_manage
whois.aeda.net.ae : ae_manage
whois.nic.ag : general_manage"""
    db_whois_addr.connect()
    whois_addr_list = []
    for line in str.split('\n'):
        whois_addr_list.append(line.split(':')[0].strip())
    for one_whois_addr in whois_addr_list:
        results = whois_addr.select().where(
            whois_addr.addr==one_whois_addr
        )
        for result in results:
            exec('print DomainAnalyse(\'{tld}\').get_punycode_tld()'.format(tld=result.tld.encode('utf-8')))
    db_whois_addr.close()

























# import shelve
# import re


# a = """addPeriod
# autoRenewPeriod
# inactive
# ok
# pendingCreate
# pendingDelete
# pendingRenew
# pendingRestore
# pendingTransfer
# pendingUpdate
# redemptionPeriod
# renewPeriod
# serverDeleteProhibited
# serverHold
# serverRenewProhibited
# serverTransferProhibited
# serverUpdateProhibited
# transferPeriod
# clientDeleteProhibited
# clientHold
# clientRenewProhibited
# clientTransferProhibited
# clientUpdateProhibited
# ACTIVE
# REGISTRY-LOCK
# REGISTRAR-LOCK
# REGISTRY-HOLD
# REGISTRAR-HOLD
# REDEMPTIONPERIOD
# PENDINGRESTORE
# PENDINGDELETE"""
# i = 1
# for line in a.split('\n'):
#     while line.find(' ') != -1:
#         line = line.replace(' ', '')
#     while line.find('-') != -1:
#         line = line.replace('-', '')
#     print '\'' + line.upper() + '\': \'' + str(i) + '\','
#     i += 1









# a = """1月 JANUARY JAN.
# 2月 FEBRUARY FEB.
# 3月 MARCH MAR.
# 4月 APRIL APR.
# 5月 MAY MAY.
# 6月 JUNE JUNE
# 7月 JULY JULY
# 8月 AUGUST AUG.
# 9月 SEPTEMBER SEP.
# 10月 OCTOBER OCT.
# 11月 NOVEMBER NOV.
# 12月 DECEMBER DEC."""

# i = 1
# for line in a.split('\n'):
#     print '\'' + line.split(' ')[2].upper().strip('.'),
#     # for char in line:
#     #     if char.isalpha():
#     #         print char,

#     print '\': ',
#     print '\'' + str(i) + '\','
#     i += 1
























# a = """
# OK  1
# INACTIVE    2
# CLIENTTRANSFERPROHIBITED   3
# CLIENTDELETEPROHIBITED    4
# CLIENTRENEWPROHIBITED    5
# CLIENTUPDATEPROHIBITED  6
# PENDINGTRANSFER    7
# PENDINGUPDATE   8
# PENDINGRENEW    9
# PENDINGDELETE  10
# SERVERHOLD   11
# CLIENTHOLD   12
# SERVERDELETEPROHIBITED    13
# SERVERUPDATEPROHIBITED    14
# SERVERTRANSFER PROHIBITED    15
# SERVERRENEW PROHIBITED   16
# SERVERLOCK   17
# CLIENTDELETEPROHIBITED   18
# CLIENTUPDATEPROHIBITED    19
# CLIENTTRANSFERPROHIBITED  20
# CLIENTLOCK   21
# REDEMPTIONPERIOD   22
# PENDINGRESTORE   23
# ACTIVE   24
# REGISTRYLOCK   25
# REGISTRARLOCK  26
# REGISTRYHOLD   27
# REGISTRARHOLD  28
# REDEMPTIONPERIOD    29
# PENDINGRESTORE  30
# PENDINGDELETE   31
# """

# for line in a.split('\n'):
#     out = ''
#     infos = re.split(r' ', line)
#     out += '\''
#     i = 0
#     while i < len(infos) - 2:
#         out += infos[i]
#         out += ' ' 
#         i += 1
#     out = out.strip()
#     out += '\': \''
#     out += infos[len(infos) - 1]
#     out += '\''
#     print out + ','

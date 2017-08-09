# -*- coding: utf8 -*-
import sys,os
from peewee import *

database = MySQLDatabase('malicious_domain_sys', **{'host': '172.26.253.3', 'password': 'platform', 'port': 3306, 'user': 'root'})

class BaseModel(Model):
    class Meta:
        database = database

# domain_index表
class domain_index(BaseModel):
    ID = BigIntegerField(primary_key=True)
    domain = CharField(null=False)
    whois_flag = IntegerField(default=0)
    locate_flag = IntegerField(default=0)
    other_info_flag = IntegerField(default=0)
    malicious_info_flag = IntegerField(default=0)
    funnel_level = IntegerField(default=0)
    judge_flag = IntegerField(default=0)
    judge_rank = IntegerField(default=0)
    source = IntegerField(default=0)
    insert_time = DateTimeField()

#  whois表
class whois(BaseModel):
    ID = BigIntegerField(primary_key=True)
    flag = IntegerField(default=0)
    domain = CharField(null=False)
    tld = CharField(null=False)
    domain_status = TextField(null=True)
    sponsoring_registrar = CharField(null=False)
    top_whois_server = CharField(null=False)
    sec_whois_server = CharField(null=False)
    reg_name = CharField(null=False)
    reg_phone = CharField(null=False)
    reg_email = CharField(null=False)
    org_name = CharField(null=False)
    name_server = TextField(null=True)
    creation_date = CharField(null=False)
    expiration_date = CharField(null=False)
    updated_date = CharField(null=False)
    details = TextField(null=True)
    insert_time = DateTimeField()

# reg_info_black_list表
class reg_info_black_lists(BaseModel):
    id = IntegerField(primary_key=True)
    flag = IntegerField(null=False)
    info = CharField(null=False)
    type = IntegerField(null=False)
    relation = CharField(null=False)
    malicious_count = IntegerField(null=False)
    domain_count = IntegerField(null=False)

# ip_history表
class ip_history1(BaseModel):
    ID = BigIntegerField(default=0)
    IP = CharField(null=False)
    record_time = DateTimeField()

# malicious_info表
class malicious_info(BaseModel):
    ID = BigIntegerField(primary_key=True, null=False)
    flag = IntegerField(null=False)
    available = IntegerField(null=False)
    HTTPcode = IntegerField(null=False)
    title = CharField(null=False)
    judge_grade = IntegerField(null=False)
    key_word = CharField(null=False)
    malicious_keywords = CharField(null=False)
    influence = IntegerField(null=False)
    influence_last_update = DateTimeField(null=True)
    IP = CharField(null=False)
    IP_detect_time = DateTimeField(null=True)
    malicious_link = TextField(null=False)
    insert_time = DateTimeField(null=False)


# locate表
class locate(BaseModel):
    ID = BigIntegerField(primary_key=True, null=False)
    flag = IntegerField(null=False)
    country = CharField(null=False)
    country_code = CharField(null=False)
    province = CharField(null=False)
    city = CharField(null=False)
    postal_code = CharField(null=False)
    street = CharField(null=False)
    reg_whois_province = CharField(null=False)
    reg_whois_city = CharField(null=False)
    reg_phone_province = CharField(null=False)
    reg_phone_city = CharField(null=False)
    reg_postal_county = CharField(null=False)
    reg_postal_province = CharField(null=False)
    reg_postal_city = CharField(null=False)
    IP = CharField(null=False)
    ICP = CharField(null=False)
    ICP_province = CharField(null=False)
    insert_time = DateTimeField(null=False)
    IP_info = CharField(null=False)
    cmp = IntegerField(null=False)
    cmpinfo = CharField(null=False)

class other_info(BaseModel):
    ID = BigIntegerField(primary_key=True, null=False)
    flag = IntegerField(null=False)
    Alex = CharField(null=False)
    Alex_last_update = DateTimeField(null=True)
    web_judge_result = IntegerField(null=False)
    appears_location = CharField(null=False)
    insert_time = DateTimeField(null=False)

class malicious_link(BaseModel):
    url_id = BigIntegerField(primary_key=True, null=False)
    url = CharField(null=False)
    url_domain = CharField(null=True)
    type = IntegerField(null=False)
    Alex = CharField(null=False)
    level = IntegerField(null=False)
    insert_time = DateTimeField(null=False)

class malicious_type(BaseModel):
    id = IntegerField(primary_key=True, null=False)
    type = CharField(null=False)
    tend_avg = TextField(null=False)
    start_date = CharField(null=False)
    end_date = CharField(null=False)
    record_time = DateTimeField(null=False)

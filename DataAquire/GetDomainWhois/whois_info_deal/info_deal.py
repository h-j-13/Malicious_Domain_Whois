#!/usr/bin/python
# encoding:utf-8

#
# 服务器返回数据处理
# @author wangkai
#


import function
from domain_status import get_status_value
from static import Static

logger = Static.logger



# 进行数据处理, 获取处理结果
# param domain_info 域名信息字典，包括域名信息，whois完整信息，whois服务器信息
# return 域名whois信息字典
def get_deal_result(domain_whois, func_name, result_flag):
    # 表示没有故障信息
    if result_flag[1] == '0':
        try:
            domain_whois = eval('function.{func_name}(domain_whois["details"], domain_whois)'.format(
                    func_name=func_name))
        except Exception as e:
            logger.error('domain: ' + domain_whois['domain'] + ' info_deal>error_info: ' + str(e))
        else:
            domain_whois['flag'] = int(result_flag + flag_manage(domain_whois), 2)  # 标记位确定
            domain_whois['domain_status'] = get_status_value(domain_whois['domain_status'],
                                                             domain_whois['domain'])  # 状态值确定
            domain_whois['whois_hash'] = hash(
                    domain_whois['reg_name'] + domain_whois['reg_phone'] + domain_whois['reg_email'] + domain_whois[
                        'org_name'] +
                    domain_whois['creation_date'] + domain_whois['expiration_date'] + domain_whois['updated_date']
            )  # whois信息哈希值
            return domain_whois

    # 一级服务器存在故障信息
    elif result_flag[2:5] != '000':
        domain_whois['flag'] = int(result_flag + '000000000', 2)
        return domain_whois
    # 二级服务器存在故障信息
    elif result_flag[5:9] != '000':
        domain_whois = function.general_manage(domain_whois['details'], domain_whois)
        domain_whois['flag'] = int(result_flag + flag_manage(domain_whois), 2)
        return domain_whois
    else:
        logger.error('result_flag error domain: ' + domain_whois['domain'] + "result_flag: " + result_flag)
        return

# 获取whois信息标志
def flag_manage(domain_whois):
    result = ''
    result += '0' if domain_whois['reg_name'] == '' else '1'
    result += '0' if domain_whois['reg_phone'] == '' else '1'
    result += '0' if domain_whois['reg_email'] == '' else '1'
    result += '0' if domain_whois['org_name'] == '' else '1'
    result += '0' if domain_whois['creation_date'] == '' else '1'
    result += '0' if domain_whois['expiration_date'] == '' else '1'
    result += '0' if domain_whois['updated_date'] == '' else '1'
    result += '0' if domain_whois['name_server'] == '' else '1'
    result += '0' if domain_whois['sponsoring_registrar'] == '' else '1'
    return result

# def special_server_manage(data, domain_whois, sec_whois_server):
#     """
#     特殊二级服务器返回格式处理
#     """
#     if sec_whois_server == 'whois.do-reg.jp':
#         domain_whois = sec_do_reg_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.enetica.com.au':
#         domain_whois = sec_enetica_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.aitdomains.com':
#         domain_whois = sec_aitdomains_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.ibi.net':
#         domain_whois = sec_ibi_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.networking4all.com':
#         domain_whois = sec_networking4all_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.dotroll.com':
#         domain_whois = sec_dotroll_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.ownidentity.com':
#         domain_whois = sec_ownidentity_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.51web.hk':
#         domain_whois = sec_51web_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.serveisweb.com':
#         domain_whois = sec_serveisweb_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.ownregistrar.com':
#         domain_whois = sec_ownregistrar_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.ksdom.kr':
#         domain_whois = sec_ksdom_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.nayana.com':
#         domain_whois = sec_nayana_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.allglobalnames.com':
#         domain_whois = sec_allglobalnames_manage(data, domain_whois)
#     elif sec_whois_server == 'comnet-whois.humeia.com':
#         domain_whois = sec_humeia_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.arcticnames.com':
#         domain_whois = sec_arcticnames_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.domains.domreg.lt':
#         domain_whois = sec_domreg_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.nordreg.com':
#         domain_whois = sec_nordreg_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.chinanet.cc':
#         domain_whois = sec_chinanet_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.afriregister.com' or sec_whois_server == 'whois.internetdomainnameregistrar.org':
#         domain_whois = sec_afriregister_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.oiinternet.com.br':
#         domain_whois = sec_oiinternet_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.domainprocessor.com':
#         domain_whois = sec_domainprocessor_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.alices-registry.com':
#         domain_whois = sec_alices_registry_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.turbosite.com.br':
#         domain_whois = sec_turbosite_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.netdorm.com':
#         domain_whois = sec_netdorm_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.sdsns.com':
#         domain_whois = sec_sdsns_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.ilait.com':
#         domain_whois = sec_ilait_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.badger.com':
#         domain_whois = sec_badger_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.binero.se':
#         domain_whois = sec_binero_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.dotearth.com':
#         domain_whois = sec_dotearth_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.maprilis.com.vn':
#         domain_whois = sec_maprilis_manage(data, domain_whois)
#     elif sec_whois_server == 'nswhois.domainregistry.com':
#         domain_whois == sec_domainregistry_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.worldbizdomains.com':
#         domain_whois == sec_worldbizdomains_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.domainguardians.com':
#         domain_whois = sec_domainguardians_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.boterosolutions.net':
#         domain_whois = sec_boterosolutions_manage(data, domain_whois)
#     elif sec_whois_server == 'whois.experianinteractive.com':
#         domain_whois = sec_experianinteractive_manage(data, domain_whois)
#
#     return domain_whois
#
#
# def sec_manage(data, domain_whois, sec_whois_server):
#     """
#     存在二级服务器的 提取函数
#     """
#
#     special_server = ['whois.do-reg.jp', 'whois.enetica.com.au', 'whois.aitdomains.com',
#                       'whois.ibi.net', 'whois.networking4all.com', 'whois.dotroll.com', 'whois.ownidentity.com',
#                       'whois.51web.hk', 'whois.serveisweb.com', 'whois.ownregistrar.com', 'whois.ksdom.kr',
#                       'whois.nayana.com', 'whois.allglobalnames.com', 'comnet-whois.humeia.com',
#                       'whois.arcticnames.com',
#                       'whois.domains.domreg.lt', 'whois.nordreg.com', 'whois.chinanet.cc', 'whois.afriregister.com',
#                       'whois.oiinternet.com.br', 'whois.internetdomainnameregistrar.org', 'whois.domainprocessor.com',
#                       'whois.alices-registry.com', 'whois.turbosite.com.br', 'whois.netdorm.com', 'whois.sdsns.com',
#                       'whois.ilait.com', 'whois.badger.com', 'whois.binero.se', 'whois.dotearth.com',
#                       'whois.maprilis.com.vn',
#                       'nswhois.domainregistry.com', 'whois.worldbizdomains.com', 'whois.domainguardians.com',
#                       'whois.boterosolutions.net',
#                       'whois.experianinteractive.com']
#
#     if sec_whois_server in special_server:  # 特殊二级服务器检验
#         domain_whois = special_server_manage(data, domain_whois, sec_whois_server)
#     else:
#         domain_whois = function.general_manage(data, domain_whois)
#
#     return domain_whois




#
#
# def academy_manage(data, domain_whois):
#     """
#     .academy, .af, .agency, .alsace,.audio 以及whois服务器为whois.donuts.co，whois-dub.mm-registry.com等的提取函
#     """
#
#     pattern = re.compile(
#             r'(Registrant Phone:.*|Registrant Name:.*|Registrant Organization:.*|Registrant Email:.*|Updated Date:.*|Creation Date:.*|Registry Expiry Date:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registrant Phone':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Name':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Email':
#                 domain_whois['reg_email'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Phone':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Organization':
#                 domain_whois['org_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Updated Date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Creation Date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registry Expiry Date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def aero_manage(data, domain_whois):
#     """
#     .aero提取函数
#     """
#
#     pattern = re.compile(
#             r'(Registrant Name:.*|Registrant Organization:.*|Registrant Email:.*|Registrant Phone:.*|Updated On:.*|Created On:.*|Expires On:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registrant Phone':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Name':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Email':
#                 domain_whois['reg_email'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Organization':
#                 domain_whois['org_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Updated On':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Created On':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Expires On':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def ag_manage(data, domain_whois):
#     """
#     .ag，.gi, mobi, museum, same ,with, gi, post, pro, sc提取函数
#     """
#
#     pattern = re.compile(
#             r'(Registrant Name:.*|Registrant Organization:.*|Registrant Email:.*|Registrant Phone:.*|Last Updated On:.*|Created On:.*|Expiration Date:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registrant Phone':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Name':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Email':
#                 domain_whois['reg_email'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Organization':
#                 domain_whois['org_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Last Updated On':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Created On':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Expiration Date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def ai_manage(data, domain_whois):
#     """
#     .ai提取函数
#     """
#
#     pos = data.find("Administrative Contact")
#
#     data_new = data[:pos]
#
#     pattern = re.compile(
#             r'(Registrant Name:.*|Organization Name..........:.*)')
#     match = pattern.findall(data_new)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registrant Name':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Organization Name..........':
#                 domain_whois['org_name'] = match[i].split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def am_manage(data, domain_whois):
#     """
#     .am提取函数
#     """
#     pattern = re.compile(
#             r'(Registrant:\n.*|Last modified:.*|Registered:.*|Expires:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split('\n')[0].strip() == 'Registrant:':
#                 domain_whois['reg_name'] = match[i].split('\n')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Last modified':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registered':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Expires':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def as_manage(data, domain_whois):
#     """
#     .as提取函数
#     """
#     pattern = re.compile(
#             r'(Registrant:\n.*|Registered on.*|Registry fee due on.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split('\n')[0].strip() == 'Registrant:':
#                 domain_whois['reg_name'] = match[i].split('\n')[1].strip()
#             elif match[i].find('Registered on') != -1:
#                 domain_whois['creation_date'] = match[i].replace("Registered on", "").strip()
#             elif match[i].find('Registry fee due on') != -1:
#                 domain_whois['expiration_date'] = match[i].replace("Registry fee due on", "").strip()
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def asia_manage(data, domain_whois):
#     """
#     .asia, .me提取函数
#     """
#
#     pattern = re.compile(
#             r'(Registrant Phone:.*|Registrant Name:.*|Registrant Organization:.*|Registrant E-mail:.*|Updated Date:.*|Create Date:.*|Expiration Date:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registrant Phone':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Name':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant E-mail':
#                 domain_whois['reg_email'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Phone':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Organization':
#                 domain_whois['org_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Updated Date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Create Date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Expiration Date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def ax_manage(data, domain_whois):
#     """
#     .ax提取函数
#     """
#
#     pattern = re.compile(
#             r'(\nName:.*|Organization:.*|Email address:.*|Telephone:.*|Created:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Name':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Email address':
#                 domain_whois['reg_email'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Telephone':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Organization':
#                 domain_whois['org_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Created':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def gd_manage(data, domain_whois):
#     """
#     .gd提取函数
#     """
#
#     pattern = re.compile(
#             r'(owner-phone:.*|owner-name:.*|owner-organization:.*|owner-email:.*|updated date:.*|created date:.*|expiration date:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'owner-phone':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'owner-name':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'owner-email':
#                 domain_whois['reg_email'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'owner-organization':
#                 domain_whois['org_name'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'updated date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'created date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'expiration date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def md_manage(data, domain_whois):
#     """
#     .md 提取函数
#     """
#
#     pattern = re.compile(
#             r'(Registrant:.*|Created:.*|Expiration date:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registrant':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Created':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Expiration date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def li_manage(data, domain_whois):
#     """
#     .li提取函数
#     """
#
#     pattern = re.compile(
#             r'(Holder of domain name:(\n.*){1}|First registration date:(\n.*){1})')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].split(':')[0].strip() == 'Holder of domain name':
#                 domain_whois['reg_name'] = match[i][0].split('\n')[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'First registration date':
#                 domain_whois['creation_date'] = match[i][0].split('\n')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def lu_manage(data, domain_whois):
#     """
#     .lu 提取函数
#     """
#
#     pattern = re.compile(
#             r'(org-name:.*|registered:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'org-name':
#                 domain_whois['org_name'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'registered':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def hk_manage(data, domain_whois):
#     """
#     .hk 提取函数
#     """
#
#     pattern = re.compile(
#             r'(Company English Name.*:.*|Email:.*|Domain Name Commencement Date:.*|Expiry Date:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Email':
#                 domain_whois['reg_email'] = match[i].split(':')[1].strip()
#             elif match[i].split('(')[0].strip() == 'Company English Name':
#                 domain_whois['org_name'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Domain Name Commencement Date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Expiry Date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def uk_manage(data, domain_whois):
#     """
#     .uk 提取函数
#     """
#     pattern = re.compile(
#             r'(Registrant:[\s\S]*?[a-z].*|Relevant dates:([\s\S]*?[a-z].*){3})')
#     match = pattern.findall(data)
#     match_length = len(match)
#     # print match
#     # print match[0][0].split(':')[1]
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].split(':', 1)[0].strip() == 'Registrant':  # Registrant name
#                 domain_whois['reg_name'] = match[i][0].split('\n', 1)[1].strip()
#
#             elif match[i][0].split(':', 1)[0].strip() == 'Relevant dates':  # date  information
#                 time_data = match[i][0].split('\r\n')
#                 time_data_lenth = len(time_data)
#                 j = 0
#                 for j in range(time_data_lenth):
#                     if time_data[j].split(':')[0].strip() == 'Registered on':
#                         domain_whois['creation_date'] = time_data[j].split(':', 1)[1].strip()
#                     elif time_data[j].split(':')[0].strip() == 'Expiry date':
#                         domain_whois['expiration_date'] = time_data[j].split(':', 1)[1].strip()
#                     elif time_data[j].split(':')[0].strip() == 'Last updated':
#                         domain_whois['updated_date'] = time_data[j].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def ceo_manage(data, domain_whois):
#     """
#     .ceo提取函数
#     """
#
#     pattern = re.compile(
#             r'(.*?Registrant Name:.*|Registrant Phone Number:.*|Registrant Email:.*|Registrant Organization:.*|Registration Date:.*|Expiration Date:.*|Last Updated Date:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     # print match
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':', 1)[0].strip() == 'Registrant Name':
#                 domain_whois['reg_name'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Registrant Phone Number':
#                 domain_whois['reg_phone'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Registrant Email':
#                 domain_whois['reg_email'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Registrant Organization':
#                 domain_whois['org_name'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Registration Date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Expiration Date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Last Updated Date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def vu_manage(data, domain_whois):
#     """
#     .vu提取函数
#     """
#     pattern = re.compile(
#             r'(First Name:.*|Last Name:.*|Date Created:.*|Expiry date:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':', 1)[0].strip() == 'First Name':
#                 first_name = match[i].split(':', 1)[1].strip()
#             if match[i].split(':', 1)[0].strip() == 'Last Name':
#                 last_name = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Date Created':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Expiry date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['reg_name'] = first_name + " " + last_name
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def ws_manage(data, domain_whois):
#     """
#     .ws提取函数
#     """
#
#     pattern = re.compile(
#             r'(Updated Date:.*|Creation Date:.*|Registrar Registration Expiration Date:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':', 1)[0].strip() == 'Creation Date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Registrar Registration Expiration Date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Updated Date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def ca_manage(data, domain_whois):
#     """
#     .ca 提取函数
#     """
#     pattern = re.compile(
#             r'(Creation date:.*|Expiry date:.*|Updated date:.*|Registrant:[\s\S]*?\n\n)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':', 1)[0].strip() == 'Registrant':
#
#                 pattern_1 = re.compile('Name:.*|Phone:.*|Email:.*')
#                 match_1 = pattern_1.findall(match[i])
#                 match_1_len = len(match_1)
#                 j = 0
#                 for j in range(match_1_len):
#                     if match_1[j].split(':')[0] == 'Name':
#                         domain_whois['reg_name'] = match_1[j].split(':')[1].strip()
#                     elif match_1[j].split(':')[0] == 'Phone':
#                         domain_whois['reg_phone'] = match_1[j].split(':')[1].strip()
#                     elif match_1[j].split(':')[0] == 'Email':
#                         domain_whois['reg_email'] = match_1[j].split(':')[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Creation date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Expiry date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Updated date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def moe_manage(data, domain_whois):
#     """
#     .moe提取函数
#     """
#
#     pattern = re.compile(
#             r'(Registrant Phone Number:.*|Registrant Name:.*|Registrant Organization:.*|Registrant Email:.*|Domain Last Updated Date:.*|Domain Expiration Date:.*|Domain Registration Date:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registrant Phone Number':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Name':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Email':
#                 domain_whois['reg_email'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Organization':
#                 domain_whois['org_name'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Domain Last Updated Date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Domain Registration Date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Domain Expiration Date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def mx_manage(data, domain_whois):
#     """
#     .mx提取函数
#     """
#
#     pattern = re.compile(
#             r'(Last Updated On:.*|Created On:.*|Expiration Date:.*|Registrant:[\s\S]*?Administrative)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':', 1)[0].strip() == 'Registrant':
#                 pattern_1 = re.compile(r'(Name:.*)')
#                 match_1 = pattern_1.findall(match[i])
#                 match_1_length = len(match_1)
#                 j = 0
#                 for j in range(match_1_length):
#                     if match_1[j].split(':')[0].strip() == 'Name':
#                         domain_whois['reg_name'] = match_1[j].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Last Updated On':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Created On':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Expiration Date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def nc_manage(data, domain_whois):
#     """
#     .nc 提取函数
#     """
#     pattern = re.compile(
#             r'(Registrant name.*|Last updated on.*|Created on.*|Expires on.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registrant name':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Last updated on':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Created on':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Expires on':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def nrw_manage(data, domain_whois):
#     """
#     nrw， scot提取函数
#     """
#     pattern = re.compile(
#             r'(Registrant Phone:.*|Registrant Name:.*|Registrant Organization:.*|Registrant Email:.*|Update Date:.*|Creation Date:.*|Registry Expiry Date:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registrant Phone':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Name':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Email':
#                 domain_whois['reg_email'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Organization':
#                 domain_whois['org_name'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Update Date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Creation Date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registry Expiry Date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def om_manage(data, domain_whois):
#     """
#     .om 提取函数
#     """
#     pattern = re.compile(
#             r'(Registrant Contact Name:.*|Registrant Contact Email:.*|Last Modified:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registrant Contact Name':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Contact Email':
#                 domain_whois['reg_email'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Last Modified':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def pe_manage(data, domain_whois):
#     """
#     .pe提取函数
#     """
#
#     pattern = re.compile(
#             r'(Registrant:(\n.*){1})')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].split(':')[0].strip() == 'Registrant':
#                 domain_whois['reg_name'] = match[i][0].split('\n')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def pf_manage(data, domain_whois):
#     """
#     .pf 提取函数
#     """
#
#     pattern = re.compile(
#             r'(Registrant Name.*|Registrant Company Name.*|Last renewed.*|Created.*|Expire.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registrant Name':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Company Name':
#                 domain_whois['org_name'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Last renewed (JJ/MM/AAAA)':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Created (JJ/MM/AAAA)':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Expire (JJ/MM/AAAA)':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def pl_manage(data, domain_whois):
#     """
#     .pl 处理函数
#     """
#
#     pattern = re.compile(
#             r'(phone:.*|company:.*|Registrant Email:.*|renewal date:.*|created:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'phone':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'company':
#                 domain_whois['org_name'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'renewal date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'created':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def ro_manage(data, domain_whois):
#     """
#     .ro提取函数
#     """
#
#     pattern = re.compile(
#             r'(Registered On:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registered On':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def rs_manage(data, domain_whois):
#     """
#     .rs 提取函数
#     """
#     pattern = re.compile(
#             r'(Registrant:.*|Modification date:.*|Registration date:.*|Expiration date:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registrant':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Modification date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registration date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Expiration date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def se_manage(data, domain_whois):
#     """
#     .se 提取函数
#     """
#
#     pattern = re.compile(
#             r'(holder:.*|modified:.*|created:.*|expires:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'holder':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'modified':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'created':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'expires':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def st_manage(data, domain_whois):
#     """
#     .st提取函数
#     """
#     pattern = re.compile(
#             r'(registrant-phone:.*|registrant-name:.*|registrant-organization:.*|registrant-email:.*|updated-date:.*|created-date:.*|expiration-date:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'registrant-phone':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'registrant-name':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'registrant-email':
#                 domain_whois['reg_email'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'registrant-organization':
#                 domain_whois['org_name'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'updated-date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'created-date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'expiration-date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def ua_manage(data, domain_whois):
#     """
#     .ua 提取函数
#     """
#     pattern = re.compile(
#             r'(% Registrant:[\s\S]%[\s\S]*?%|created:.*[\s\S]modified:.*[\s\S]expires:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#
#     for i in range(match_length):
#         if match[i].split()[0] == '%':  # Registrant information
#
#             pattern_1 = re.compile('person:.*|phone:.*|e-mail:.*|organization:.*')
#             match_1 = pattern_1.findall(match[i])
#             match_1_len = len(match_1)
#             j = 0
#             for j in range(match_1_len):
#                 if match_1[j].split(':')[0] == 'person':
#                     domain_whois['reg_name'] = match_1[j].split(':')[1].strip()
#                 elif match_1[j].split(':')[0] == 'phone':
#                     domain_whois['reg_phone'] = match_1[j].split(':')[1].strip()
#                 elif match_1[j].split(':')[0] == 'e-mail':
#                     domain_whois['reg_email'] = match_1[j].split(':')[1].strip()
#                 elif match_1[j].split(':')[0] == 'organization':
#                     domain_whois['org_name'] = match_1[j].split(':')[1].strip()
#
#         elif match[i].split(':')[0] == 'created':  # Date information
#             pattern_2 = re.compile(
#                     r'created:.*|modified:.*|expires:.*')
#             match_2 = pattern_2.findall(match[i])
#             match_2_len = len(match_2)
#             j = 0
#             for j in range(match_2_len):
#                 if match_2[j].split(':')[0] == 'created':
#                     domain_whois['creation_date'] = match_2[j].split(':', 1)[1].strip()
#                 elif match_2[j].split(':')[0] == 'expires':
#                     domain_whois['expiration_date'] = match_2[j].split(':', 1)[1].strip()
#                 elif match_2[j].split(':')[0] == 'modified':
#                     domain_whois['updated_date'] = match_2[j].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def cf_manage(data, domain_whois):
#     """
#     .cf 提取函数
#     """
#     pattern = re.compile(
#             r'(Owner contact:[\s\S]*?\n\n|Domain registered:.*|Record will expire on:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':', 1)[0].strip() == 'Owner contact':
#
#                 pattern_1 = re.compile('Name:.*|Phone:.*|E-mail:.*|Organization:.*')
#                 match_1 = pattern_1.findall(match[i])
#                 match_1_len = len(match_1)
#                 j = 0
#                 for j in range(match_1_len):
#                     if match_1[j].split(':')[0] == 'Name':
#                         domain_whois['reg_name'] = match_1[j].split(':')[1].strip()
#                     elif match_1[j].split(':')[0] == 'Phone':
#                         domain_whois['reg_phone'] = match_1[j].split(':')[1].strip()
#                     elif match_1[j].split(':')[0] == 'E-mail':
#                         domain_whois['reg_email'] = match_1[j].split(':')[1].strip()
#                     elif match_1[j].split(':', 1)[0].strip() == 'Organization':
#                         domain_whois['org_name'] = match_1[j].split(':')[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Domain registered':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Record will expire on':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def ci_manage(data, domain_whois):
#     """
#     ci 提取函数
#     """
#
#     pattern = re.compile(
#             r'''(Owner's handle:.*|Created:.*|Expiration date:.*)''')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':', 1)[0].strip() == '''Owner's handle''':
#                 domain_whois['reg_name'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Created':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Expiration date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def club_manage(data, domain_whois):
#     """
#     .club 提取函数
#     """
#     pattern = re.compile(
#             r'(Registrant Name:.*|Registrant Organization:.*|Registrant Email:.*|Registrant Phone Number:.*|Last Updated Date:.*|Registration Date:.*|Expiration Date:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     # print match
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':', 1)[0].strip() == 'Registrant Name':
#                 domain_whois['reg_name'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Registrant Phone Number':
#                 domain_whois['reg_phone'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Registrant Email':
#                 domain_whois['reg_email'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Registrant Organization':
#                 domain_whois['org_name'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Registration Date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Expiration Date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Last Updated Date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def dk_manage(data, domain_whois):
#     """
#     .dk 提取函数
#     """
#     pattern = re.compile(
#             r'(Registered:.*|Expires:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':', 1)[0].strip() == 'Registered':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Expires':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def dm_manage(data, domain_whois):
#     """
#     dm 提取函数
#     """
#     pattern = re.compile(
#             r'(owner-name:.*|owner-organization:.*|owner-phone:.*|owner-email:.*|created date:.*|updated date:.*|expiration date:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':', 1)[0].strip() == 'owner-name':
#                 domain_whois['reg_name'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'owner-phone':
#                 domain_whois['reg_phone'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'owner-email':
#                 domain_whois['reg_email'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'owner-organization':
#                 domain_whois['org_name'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'created date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'expiration date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'updated date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def ec_manage(data, domain_whois):
#     """
#     .ec提取函数
#     """
#
#     pattern = re.compile(
#             r'(Registrant:[\s\S]*?\n\n|Created:.*|Modified:.*|Expires:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':', 1)[0].strip() == 'Registrant':
#
#                 pattern_1 = re.compile('Name:.*|Phone Number:.*|Email Address:.*|Organisation:.*')
#                 match_1 = pattern_1.findall(match[i])
#                 match_1_len = len(match_1)
#                 j = 0
#                 for j in range(match_1_len):
#
#                     if match_1[j].split(':')[0] == 'Name':
#                         domain_whois['reg_name'] = match_1[j].split(':')[1].strip()
#                     elif match_1[j].split(':')[0] == 'Phone Number':
#                         domain_whois['reg_phone'] = match_1[j].split(':')[1].strip()
#                     elif match_1[j].split(':')[0] == 'Email Address':
#                         domain_whois['reg_email'] = match_1[j].split(':')[1].strip()
#                     elif match_1[j].split(':')[0].strip() == 'Organisation':
#                         domain_whois['org_name'] = match_1[j].split(':')[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Created':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Expires':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Modified':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def tn_manage(data, domain_whois):
#     """
#     tn 提取函数
#     """
#     pattern = re.compile(
#             r'(First Name:.*|Last Name:.*|Activation:.*|Tel:.*|e-mail:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':', 1)[0].strip() == 'First Name':
#                 First_Name = match[i].split(':.........', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Last Name':
#                 Last_Name = match[i].split(':..........', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Tel':
#                 domain_whois['reg_phone'] = match[i].split(':................', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'e-mail':
#                 domain_whois['reg_email'] = match[i].split(':.............', 1)[1].strip()
#             elif match[i].split(':', 1)[0].strip() == 'Activation':
#                 domain_whois['creation_date'] = match[i].split(':.........', 1)[1].strip()
#         if First_Name or Last_Name:
#             domain_whois['reg_name'] = First_Name + ' ' + Last_Name
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def osaka_manage(data, domain_whois):
#     """
#     .osaka， .party, .science提取函数
#     """
#
#     pattern = re.compile(
#             r'(Registrant Phone Number:.*|Registrant Name:.*|Registrant Organization:.*|Registrant Email:.*|Domain Last Updated Date:.*|Domain Registration Date:.*|Domain Expiration Date:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registrant Phone Number':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Name':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Email':
#                 domain_whois['reg_email'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Organization':
#                 domain_whois['org_name'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Domain Last Updated Date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Domain Registration Date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Domain Expiration Date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def tw_manage(data, domain_whois):
#     """
#     .tw后缀提取函数
#     """
#     if data.find("Administrative Contact:") != -1:
#         pattern = re.compile(r'(Registrant:\n.*\n.*\n.*|Record created on.*|Record expires on.*)')
#         match = pattern.findall(data)
#         match_length = len(match)
#         i = 0
#         if match:
#             for i in range(match_length):
#                 if match[i].find('Registrant') != -1:
#                     info = match[i].split("\n")
#                     domain_whois['org_name'] = info[1].strip()
#                     domain_whois['reg_name'] = info[2].split('  ')[0].strip()
#                     domain_whois['reg_email'] = info[2].split('  ')[1].strip()
#                     domain_whois['reg_phone'] = info[3].strip()
#                 elif match[i].split("on")[0].strip() == 'Record created':
#                     domain_whois['creation_date'] = match[i].split(' ', )[3].strip()
#                 elif match[i].split('on')[0].strip() == 'Record expires':
#                     domain_whois['expiration_date'] = match[i].split(' ')[3].strip()
#
#         domain_whois['details'] = str(data)
#         return domain_whois
#
#     pattern = re.compile(
#             r'(Registrant:.*\n.*\n.*|.*\n.*TEL:.*|Record created on.*|Record expires on.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if len(match[i].split(r'TEL:')) > 1:
#                 info = match[i].split('\n')[0].strip().split('   ')
#                 if len(info) == 2:
#                     domain_whois['reg_name'] = info[0]
#                     domain_whois['reg_email'] = info[1]
#                 domain_whois['reg_phone'] = match[i].split('TEL:')[1].strip()
#             elif match[i].split("on")[0].strip() == 'Record created':
#                 domain_whois['creation_date'] = match[i].split(' ', )[3].strip()
#             elif match[i].split('on')[0].strip() == 'Record expires':
#                 domain_whois['expiration_date'] = match[i].split(' ')[3].strip()
#             elif match[i].find("Registrant:") != -1:
#                 domain_whois['org_name'] = match[i].split('\n')[2].strip()
#
#     if data.find("TEL:") == -1:
#         pattern = re.compile(r'(Contact:.*\n.*\n.*)')
#         match = pattern.findall(data)
#         if match:
#             info = match[0].split('\n')
#             if info[2] != r'( *)':
#                 sign = True
#                 for c in info[2].strip():
#                     if c.isalpha():
#                         sign = False
#                         break
#                 if sign:
#                     domain_whois['phone'] = info[2].strip()
#                     domain_whois['reg_email'] = info[1].split("   ")[0].strip()
#                     domain_whois['reg_name'] = info[1].split("   ")[1].strip()
#                 elif info[2].find('@') != -1:
#                     domain_whois['reg_name'] = info[1].strip()
#                     domain_whois['reg_email'] = info[2].strip()
#             else:
#                 domain_whois['reg_name'] = info[1].split("   ")[0].strip()
#                 domain_whois['reg_email'] = info[1].split("   ")[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def kr_manage(data, domain_whois):
#     """
#     .kr 提取函数
#     """
#
#     pos = data.find("# ENGLISH")
#     if pos == -1:
#         domain_whois['details'] = data
#         return domain_whois
#
#     new_data = data[pos:]
#     pattern = re.compile(
#             r'(Registrant                  :.*|Registered Date.*|Last Updated Date.*|Expiration Date.*)')
#     match = pattern.findall(new_data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registrant':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Last Updated Date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registered Date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Expiration Date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def ru_manage(data, domain_whois):
#     """
#     whois.tcinet.ru提取函数
#     """
#
#     pattern = re.compile(
#             r'(person:.*|org:.*|created:.*|paid-till:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'org:':
#                 domain_whois['org_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'person':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'created':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'paid-till':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sg_manage(data, domain_whois):
#     """
#     whois.sgnic.sg 提取函数
#     """
#     pattern = re.compile(
#             r'(Registrant:.*\n.*\n.*Name:.*|Creation Date:.*|Modified Date:.*|Expiration Date:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].find("Name") != -1:
#                 domain_whois['reg_name'] = match[i].split('Name:')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Modified Date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Creation Date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Expiration Date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def int_manage(data, domain_whois):
#     """
#     whois.iana.org 提取函数
#     """
#     pattern = re.compile(
#             r'(domain:.*\n\norganisation:.*|contact:.*administrative(.*\n)+?phone:(.*\n)+?e-mail:.*|created:.*|changed:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find("organisation:") != -1:
#                 domain_whois['reg_name'] = match[i][0].split('organisation:')[1].strip()
#             # 行政联系获得联系电话及邮箱
#             # elif match[i][0].find('contact:      administrative') != -1:
#             #     infos = match[i][0].split("\n")
#             #     for info in infos:
#             #         if info.find('phone:') != -1:
#             #             domain_whois['reg_phone'] = info.split(':')[1].strip()
#             #         if info.find('e-mail:') != -1:
#             #             domain_whois['reg_email'] = info.split(':')[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'changed':
#                 domain_whois['updated_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'created':
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def kz_manage(data, domain_whois):
#     """
#     whois.nic.kz 提取函数
#     """
#
#     pattern = re.compile(
#             r'(Domain created:.*|Last modified :.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Domain created':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Last modified':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#
#     pos = data.find("Administrative")
#     new_data = data[:pos]
#     pattern = re.compile(
#             r'(Name...................:.*|Organization Name......:.*)')
#     match = pattern.findall(new_data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Name...................':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Organization Name......':
#                 domain_whois['org_name'] = match[i].split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def ir_manage(data, domain_whois):
#     """
#     whois.nic.ir 提取函数
#     """
#
#     pattern = re.compile(
#             r'(holder-c:.*|last-updated:.*|expire-date:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     person_id = ''
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'last-updated':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'expire-date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'holder-c':
#                 person_id = match[i].split(':', 1)[1].strip()
#
#     pattern_2 = re.compile(r'(nic-hdl:(.*\n)+?source:.*)')
#     match_2 = pattern_2.findall(data)
#     match_length_2 = len(match_2)
#     j = 0
#     if match_2:
#         for j in range(match_length_2):
#             infos = match_2[0][0].split("\n")
#             if infos[0].split(":")[1].strip() == person_id:
#                 for info in infos:
#                     if info.split(":")[0].strip() == "person":
#                         domain_whois["reg_name"] = info.split(":")[1].strip()
#                     elif info.split(":")[0].strip() == "e-mail":
#                         domain_whois["reg_email"] = info.split(":")[1].strip()
#                     elif info.split(":")[0].strip() == "phone":
#                         domain_whois["reg_phone"] = info.split(":")[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def mk_manage(data, domain_whois):
#     """
#     whois.marnet.mk 提取物函数
#     """
#
#     pattern = re.compile(
#             r'(domain:(.*\n)+?expire:.*)')
#     match = pattern.findall(data)
#     person_id = ''
#     if match:
#         infos = match[0][0].split('\n')
#         for info in infos:
#             if info.find('registrant:') != -1:
#                 person_id = info.split(':')[1].strip()
#             elif info.find('registered:') != -1:
#                 domain_whois['creation_date'] = info.split(':', 1)[1].strip()
#             elif info.find('changed:') != -1:
#                 domain_whois['updated_date'] = info.split(':', 1)[1].strip()
#             elif info.find('expire') != -1:
#                 domain_whois['expiration_date'] = info.split(':', 1)[1].strip()
#
#     pattern_2 = re.compile(r'(contact:(.*\n)+?created:.*)')
#     match_2 = pattern_2.findall(data)
#     i = 0
#     match_length_2 = len(match_2)
#     if match_2:
#         for i in range(match_length_2):
#             infos = match_2[i][0].split('\n')
#             if infos[0].split(':')[1].strip() == person_id:
#                 for info in infos:
#                     if info.find('name:') != -1:
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#                     elif info.find('org:') != -1:
#                         domain_whois['org_name'] = info.split(':')[1].strip()
#                     elif info.find('phone:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#                     elif info.find('e-mail:') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def th_manage(data, domain_whois):
#     """
#     whois.thnic.co.th 提取函数
#     """
#
#     pattern = re.compile(
#             r'(Updated date:.*|Created date:.*|Exp date:.*|Domain Holder:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Updated date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Exp date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Created date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Domain Holder':
#                 domain_whois['reg_name'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def ae_manage(data, domain_whois):
#     """
#     whois.aeda.net.ae 提取函数
#     """
#     pattern = re.compile(
#             r'(Registrant Contact Name:.*|Registrant Contact Email:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registrant Contact Email':
#                 domain_whois['reg_email'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Contact Name':
#                 domain_whois['reg_name'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def by_manage(data, domain_whois):
#     """
#     whois.cctld.by 提取函数
#     """
#
#     pattern = re.compile(
#             r'(Updated Date:.*|Creation Date:.*|Expiration Date:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Updated Date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Creation Date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Expiration Date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def my_manage(data, domain_whois):
#     """
#     whois.mynic.my 提取函数
#     """
#
#     pattern = re.compile(
#             r'(\[Record Created\].*|\[Record Expired\].*|\[Record Last Modified\].*|\[Registrant Code\](.*\n)+?  .Fax.)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].split(']')[0].strip() == '[Record Last Modified':
#                 domain_whois['updated_date'] = match[i][0].split(']', 1)[1].strip()
#             elif match[i][0].split(']')[0].strip() == '[Record Created':
#                 domain_whois['creation_date'] = match[i][0].split(']', 1)[1].strip()
#             elif match[i][0].split(']')[0].strip() == '[Record Expired':
#                 domain_whois['expiration_date'] = match[i][0].split(']', 1)[1].strip()
#             elif match[i][0].find("[Registrant Code]") != -1:
#                 infos = match[i][0].split("\n")
#                 domain_whois['reg_name'] = infos[1]
#                 for info in infos:
#                     if info.find('(Tel)') != -1:
#                         domain_whois['reg_phone'] = info.replace('(Tel)', '').strip()
#                     elif info.find('@') != -1:
#                         domain_whois['reg_email'] = info.strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sa_manage(data, domain_whois):
#     """
#     whois.nic.net.sa 提取函数
#     """
#     pattern = re.compile(
#             r'(Registrant:\n.*|Last Updated on:.*|Created on:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].find('Registrant:') != -1:
#                 domain_whois['reg_name'] = match[i].split('\n')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Last Updated on':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Created on':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def uy_manage(data, domain_whois):
#     """
#     .uy 提取函数
#     """
#
#     pattern = re.compile(
#             r'(Titular:.*\n(.*\n)+?.*(FAX)|Ultima Actualizacion:.*|Fecha de Creacion:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('Titular:') != -1:
#                 infos = match[i][0].split('\n')
#                 name_email = infos[1].split('\t\t')
#                 domain_whois['reg_name'] = name_email[0].split('  ')[0].strip()
#                 if len(name_email) > 1:
#                     domain_whois['reg_email'] = name_email[1]
#                 for info in infos:
#                     if info.find('FAX') != -1:
#                         domain_whois['reg_phone'] = info.split('(')[0].strip()
#
#             elif match[i][0].split(':')[0].strip() == 'Ultima Actualizacion':
#                 domain_whois['updated_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'Fecha de Creacion':
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def at_manage(data, domain_whois):
#     """
#     .at 提取函数
#     """
#
#     pattern = re.compile(
#             r'(domain:(.*\n)+?source:.*|personname:(.*\n)+?source:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     person_id = ''
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('domain') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('registrant:') != -1:
#                         person_id = info.split(':')[1].strip()
#                     elif info.find('changed:') != -1:
#                         domain_whois['updated_date'] = info.split(':', 1)[1].strip()
#
#             elif match[i][0].find('personname') != -1:
#                 infos = match[i][0].split('\n')
#                 sign = False
#                 for info in infos:
#                     if info.find('nic-hdl:') != -1:
#                         if person_id == info.split(':')[1].strip():
#                             sign = True
#                 if sign:
#                     for info in infos:
#                         if info.find('phone:') != -1:
#                             domain_whois['reg_phone'] = info.split(':')[1].strip()
#                         elif info.find('e-mail:') != -1:
#                             domain_whois['reg_email'] = info.split(':')[1].strip()
#                         elif info.find('organization:') != -1:
#                             domain_whois['org_name'] = info.split(':')[1].strip()
#                         elif info.find('personname') != -1:
#                             domain_whois['reg_name'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def au_manage(data, domain_whois):
#     """
#     .au 提取函数
#     """
#
#     pattern = re.compile(
#             r'(Registrant:.*|Last Modified:.*|Registrant Contact Name:.*|Registrant Contact Email:.*|Eligibility Type:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     type_temp = ''
#     name_temp = ''
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registrant Contact Email':
#                 domain_whois['reg_email'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Contact Name':
#                 domain_whois['reg_name'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0] == 'Registrant':
#                 name_temp = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0] == 'Eligibility Type':
#                 type_temp = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Last Modified':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#
#         if type_temp == 'Company':
#             domain_whois['org_name'] = name_temp
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def be_manage(data, domain_whois):
#     """
#     be 提取函数
#     """
#
#     pattern = re.compile(
#             r'(Registered:.*)')
#     match = pattern.findall(data)
#     if match:
#         domain_whois['creation_date'] = match[0].split(':')[1].strip()
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def bg_manage(data, domain_whois):
#     """
#     bg 提取函数
#     """
#
#     pattern = re.compile(
#             r'(expires at:.*|activated on:.*|REGISTRANT:\n.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'expires at':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'activated on':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'REGISTRANT':
#                 domain_whois['reg_name'] = match[i].split('\n')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def bo_manage(data, domain_whois):
#     """
#     bo 提取函数
#     """
#     pattern = re.compile(
#             r'(TITULAR:(.*\n)+?Telefono:.*|Fecha de registro:.*|Fecha de vencimiento:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find("TITULAR") != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('Organizacion') != -1:
#                         domain_whois['org_name'] = info.split(':')[1].strip()
#                     elif info.find('Email') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#                     elif info.find('Telefono') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#                     elif info.find('Nombre') != -1:
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#
#             elif match[i][0].split(':')[0].strip() == 'Fecha de registro':
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'Fecha de vencimiento':
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def edu_manage(data, domain_whois):
#     """
#     edu 提取函数
#     """
#
#     pattern = re.compile(
#             r'(Registrant:\n.*|Domain record activated:.*|Domain record last updated:.*|Domain expires:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split('\n')[0].strip() == 'Registrant:':
#                 domain_whois['reg_name'] = match[i].split('\n')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Domain record last updated':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Domain record activated':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Domain expires':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def ee_manage(data, domain_whois):
#     """
#     ee 提取函数
#     """
#
#     pattern = re.compile(
#             r'(domain:(.*\n)+?contact)')
#     match = pattern.findall(data)
#     if match:
#         infos = match[0][0].split('\n')
#         for info in infos:
#             if info.find('registrant:') != -1:
#                 reg_id = info.split(':')[1].strip()
#             elif info.find('registered:') != -1:
#                 domain_whois['creation_date'] = info.split(':', 1)[1].strip()
#             elif info.find('changed:') != -1:
#                 domain_whois['updated_date'] = info.split(':', 1)[1].strip()
#             elif info.find('expire:') != -1:
#                 domain_whois['expiration_date'] = info.split(':', 1)[1].strip()
#
#     pattern_2 = re.compile(r'(contact:(.*\n)+?created:.*)')
#     match = pattern_2.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].split('\n')[0].split(':')[1].strip() == reg_id:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('name:') != -1:
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#                     elif info.find('e-mail:') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#                     elif info.find('org:') != -1:
#                         domain_whois['org_name'] = info.split(':')[1].strip()
#                     elif info.find('phone:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def fi_manage(data, domain_whois):
#     """
#     fi 提取函数
#     """
#     pattern = re.compile(
#             r'(descr:.*|created:.*|modified:.*|expires:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     sign = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'descr' and sign == 0:
#                 sign = 1
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'phone':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'modified':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'created':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'expires':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def fr_manage(data, domain_whois):
#     """
#     fr 提取函数
#     """
#     pattern = re.compile(
#             r'(holder-c:.*|last-update:.*|Expiry Date:.*|created:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     person_id = ''
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'last-update':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Expiry Date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'created':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'holder-c':
#                 person_id = match[i].split(':', 1)[1].strip()
#
#     pattern_2 = re.compile(r'(nic-hdl:(.*\n)+?source:.*)')
#     match_2 = pattern_2.findall(data)
#     match_length_2 = len(match_2)
#     j = 0
#     if match_2:
#         for j in range(match_length_2):
#             infos = match_2[j][0].split("\n")
#             if infos[0].split(":")[1].strip() == person_id:
#                 for info in infos:
#                     if info.split(":")[0].strip() == "e-mail":
#                         domain_whois["reg_email"] = info.split(":")[1].strip()
#                     elif info.split(":")[0].strip() == "phone":
#                         domain_whois["reg_phone"] = info.split(":")[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def gq_manage(data, domain_whois):
#     """
#     gq 提取函数
#     """
#     pattern = re.compile(
#             r'(Owner contact:(.*\n)+?.*\n|Domain registered:.*|Record will expire on:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].split(':')[0].strip() == 'Domain registered':
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             if match[i][0].split(':')[0].strip() == 'Record will expire on':
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Owner contact') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('Organization:') != -1:
#                         domain_whois['org_name'] = info.split(':')[1].strip()
#                     elif info.find('Name:') != -1:
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#                     elif info.find('Phone:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#                     elif info.find('E-mail:') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def hr_manage(data, domain_whois):
#     """
#     hr 提取函数
#     """
#     pattern = re.compile(
#             r'(descr:.*|expires:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     sign = 0
#     if match:
#         for i in range(match_length):
#             if sign == 0 and match[i].split(':')[0].strip() == 'descr':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#                 sign = 1
#             elif match[i].split(':')[0].strip() == 'expires':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def im_manage(data, domain_whois):
#     """
#     im 提取函数
#     """
#
#     pattern = re.compile(
#             r'(Domain Owners / Registrant.*\nName.*|Expiry Date:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].find('Domain Owners / Registrant') != -1:
#                 domain_whois['reg_name'] = match[i].split('Name:')[1].strip()
#             elif match[i].find('Expiry Date:') != -1:
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def is_manage(data, domain_whois):
#     """
#     is 提取函数
#     """
#
#     pattern = re.compile(
#             r'(domain:(.*\n)+?source:)')
#     match = pattern.findall(data)
#     person_id = ''
#     if match:
#         infos = match[0][0].split('\n')
#         for info in infos:
#             if info.find('registrant:') != -1:
#                 person_id = info.split(':')[1].strip()
#             elif info.find('created:') != -1:
#                 domain_whois['creation_date'] = info.split(':', 1)[1].strip()
#             elif info.find('expires:') != -1:
#                 domain_whois['expiration_date'] = info.split(':', 1)[1].strip()
#
#     pattern_2 = re.compile(r'((role|person):(.*\n)+?source)')
#     match_2 = pattern_2.findall(data)
#     match_length_2 = len(match_2)
#     i = 0
#     if match_2:
#         for i in range(match_length_2):
#             infos = match_2[i][0].split('\n')
#             if infos[1].split(':')[1].strip() == person_id:
#                 for info in infos:
#                     if info.find('person:') != -1 or info.find('role:') != -1:
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#                     elif info.find('phone:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#                     elif info.find('e-mail:') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def it_manage(data, domain_whois):
#     """
#     it 提取函数
#     """
#     pattern = re.compile(
#             r'(Domain:(.*\n)+?Expire Date:.*|Registrant(.*\n)+?.*Admin Contact)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('Domain') != -1 and match[i][0].find('Status') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.split(':')[0].strip() == 'Created':
#                         domain_whois['creation_date'] = info.split(':', 1)[1].strip()
#                     elif info.split(':')[0].strip() == 'Last Update':
#                         domain_whois['updated_date'] = info.split(':', 1)[1].strip()
#                     elif info.split(':')[0].strip() == 'Expire Date':
#                         domain_whois['expiration_date'] = info.split(':', 1)[1].strip()
#
#             elif match[i][0].find('Registrant') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('Organization:') != -1:
#                         domain_whois['org_name'] = info.split(':')[1].strip()
#                     elif info.find('Name:') != -1:
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def jp_manage(data, domain_whois):
#     """
#     jp 提取函数
#     """
#     pattern = re.compile(r'(\[Organization\].*|\[登録年月日\].*|\[接続年月日\].*|\[最終更新\].*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].find('[Organization]') != -1:
#                 domain_whois['org_name'] = match[i].split(']')[1].strip()
#             elif match[i].find('[登録年月日]') != -1:
#                 domain_whois['creation_date'] = match[i].split(']', 1)[1].strip()
#             elif match[i].find('[最終更新]') != -1:
#                 domain_whois['updated_date'] = match[i].split(']', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def lt_manage(data, domain_whois):
#     """
#     lt 提取函数
#     """
#     pattern = re.compile(
#             r'(Registered:.*)')
#
#     match = pattern.findall(data)
#     if match and match[0].split(':')[0].strip() == 'Registered':
#         domain_whois['creation_date'] = match[0].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def lv_manage(data, domain_whois):
#     pattern = re.compile(
#             r'(\[Domain\](\n.*)+?\n\n|\[Holder\](\n.*)+?\n\n)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('[Domain]') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('Changed:') != -1:
#                         domain_whois['updated_date'] = info.split(':', 1)[1].strip()
#             elif match[i][0].find('[Holder]') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('Email:') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#                     elif info.find('Phone:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#                     elif info.find('Name:') != -1:
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def ly_manage(data, domain_whois):
#     """
#     ly 提取函数
#     """
#     pattern = re.compile(
#             r'(Registrant:(\n.*)+?\n\n|Created:.*|Updated:.*|Expired:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('Registrant') != -1:
#                 infos = match[i][0].split('\n')
#                 domain_whois['reg_name'] = infos[1].strip()
#                 for info in infos:
#                     if info.find('Phone:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#                     elif info.find('@') != -1:
#                         domain_whois['reg_email'] = info.strip()
#
#             elif match[i][0].split(':')[0].strip() == 'Created':
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'Updated':
#                 domain_whois['updated_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'Expired':
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def ml_manage(data, domain_whois):
#     """
#     ml 提取函数
#     """
#     pattern = re.compile(r'(Owner contact:(\n.*)+?\n\n|Domain registered:.*|Record will expire on:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 1
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('Owner contact:') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('Organization:') != -1:
#                         domain_whois['org_name'] = info.split(':')[1].strip()
#                     elif info.find('Name:') != -1:
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#                     elif info.find('Phone:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#                     elif info.find('E-mail:') != -1:
#                         domain_whois['reg_email'] = info.split(':', 1)[1].strip()
#             elif match[i][0].find('Domain registered:') != -1:
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Record will expire on:') != -1:
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def no_manage(data, domain_whois):
#     """
#     no 提取函数
#     """
#     pattern = re.compile(
#             r'(Domain Holder Handle(.*\n)+?Last updated:.*)')
#
#     match = pattern.findall(data)
#     person_id = ''
#     if match:
#         infos = match[0][0].split('\n')
#         for info in infos:
#             if info.find('Domain Holder Handle') != -1:
#                 person_id = info.split(':')[1].strip()
#             elif info.find('Last updated:') != -1:
#                 domain_whois['updated_date'] = info.split(':', 1)[1].strip()
#             elif info.find('Created:') != -1:
#                 domain_whois['creation_date'] = info.split(':', 1)[1].strip()
#
#     pattern_2 = re.compile(r'(NORID Handle(.*\n)+?\n)')
#     match_2 = pattern_2.findall(data)
#     match_length_2 = len(match_2)
#     i = 0
#     sign = False
#     reg_type = 1
#     if match_2:
#         for i in range(match_length_2):
#             infos = match_2[i][0].split('\n')
#             for info in infos:
#                 if info.find('NORID Handle') != -1:
#                     if info.split(':')[1].strip() == person_id:
#                         sign = True
#                 elif info.find('Type.......................:') != -1:
#                     if info.split(':')[1].strip() == 'organization':
#                         reg_type = 2
#                 elif sign and info.find('Name') != -1:
#                     if reg_type == 2:
#                         domain_whois['org_name'] = info.split(':')[1].strip()
#                     else:
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#                 elif sign and info.find('Phone Number') != -1:
#                     domain_whois['reg_phone'] = info.split(':')[1].strip()
#                 elif sign and info.find('Email Address') != -1:
#                     domain_whois['reg_email'] = info.split(':')[1].strip()
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def nu_manage(data, domain_whois):
#     """
#     nu 提取函数
#     """
#     pattern = re.compile(
#             r'(created:.*|modified:.*|expires.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'created':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'modified':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'expires':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def nz_manage(data, domain_whois):
#     """
#     nz 提取函数
#     """
#     pattern = re.compile(
#             r'(domain_dateregistered:.*|domain_datelastmodified:.*|domain_datebilleduntil:.*|registrant_contact_name:.*|registrant_contact_phone:.*|registrant_contact_email:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'domain_dateregistered':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'domain_datelastmodified':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'domain_datebilleduntil':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'registrant_contact_name':
#                 domain_whois['reg_name'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'registrant_contact_phone':
#                 domain_whois['reg_phone'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'registrant_contact_email':
#                 domain_whois['reg_email'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def pm_manage(data, domain_whois):
#     """
#     pm 提取函数
#     """
#     pattern = re.compile(
#             r'(holder-c:.*|Expiry Date:.*|created:.*|last-update:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     person_id = ''
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'created':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'last-update':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Expiry Date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'holder-c':
#                 person_id = match[i].split(':')[1].strip()
#
#     pattern_2 = re.compile(r'(nic-hdl(.*\n)+?\n)')
#     match_2 = pattern_2.findall(data)
#     match_length_2 = len(match_2)
#     i = 0
#     sign = False
#     if match_2:
#         for i in range(match_length_2):
#             infos = match_2[i][0].split('\n')
#             for info in infos:
#                 if info.find('nic-hdl:') != -1:
#                     if info.split(':')[1].strip() == person_id:
#                         sign = True
#                     else:
#                         break
#                 elif sign and info.find('phone:') != -1:
#                     domain_whois['reg_phone'] = info.split(':')[1].strip()
#                 elif sign and info.find('e-mail:') != -1:
#                     domain_whois['reg_email'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def pr_manage(data, domain_whois):
#     """
#     pr 提取函数
#     """
#     pattern = re.compile(
#             r'(Created On:.*|Expires On:.*|Contact:      Registrant(.*\n)+?\n)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].split(':')[0].strip() == 'Created On':
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'Expires On':
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Contact:      Registrant') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('Organization:') != -1:
#                         domain_whois['org_name'] = info.split(':')[1].strip()
#                     elif info.find('Name:') != -1:
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#                     elif info.find('Phone:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#                     elif info.find('E-mail:') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sh_manage(data, domain_whois):
#     """
#     sh 提取函数
#     """
#     pattern = re.compile(
#             r'(Expiry.*|Owner(.*\n)+?\n)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].split(':')[0].strip() == 'Expiry':
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Owner  :') != -1:
#                 domain_whois['reg_name'] = match[i][0].split('\n')[0].split(':')[1].strip()
#                 domain_whois['org_name'] = match[i][0].split('\n')[1].split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def si_manage(data, domain_whois):
#     """
#     si 提取函数
#     """
#     pattern = re.compile(
#             r'(created:.*|expire:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'expire':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'created':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sk_manage(data, domain_whois):
#     """
#     sk 提取函数
#     """
#     pattern = re.compile(
#             r'(Last-update.*|Valid-date.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             match[i] = " ".join(match[i].split())
#             if match[i].split(' ')[0].strip() == 'Last-update':
#                 domain_whois['updated_date'] = match[i].split(' ')[1].strip()
#             elif match[i].split(' ')[0].strip() == 'Valid-date':
#                 domain_whois['expiration_date'] = match[i].split(' ')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sm_manage(data, domain_whois):
#     """
#     sm 提取函数
#     """
#     pattern = re.compile(
#             r'(Registration date:.*|Owner:(.*\n)+?\n)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].split(':')[0].strip() == 'Registration date':
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Owner:') != -1:
#                 infos = match[i][0].split('\n')
#                 domain_whois['reg_name'] = infos[2].strip()
#                 for info in infos:
#                     if info.find('Phone:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#                     elif info.find('Email:') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sn_manage(data, domain_whois):
#     """
#     sn 提取函数
#     """
#     pattern = re.compile(
#             r'(Date de creation:.*|Derniere modification:.*|Date d\'expiration:.*|Nom Registrant:.*|Telephone Registrant:.*|Courriel Registrant.:.*|)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Date de creation':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Derniere modification':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Date d\'expiration':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Nom Registrant':
#                 domain_whois['reg_name'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Telephone Registrant':
#                 domain_whois['reg_phone'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Courriel Registrant.':
#                 domain_whois['reg_email'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def so_manage(data, domain_whois):
#     """
#     so 提取函数
#     """
#     pattern = re.compile(
#             r'(Registrant Internationalized Name:.*|Registrant Internationalized Organization:.*|Registrant Email:.*|Registrant Voice Number:.*|Last Updated On:.*|Creation Date:.*|Expiration Date:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registrant Voice Number':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Internationalized Name':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Email':
#                 domain_whois['reg_email'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Internationalized Organization':
#                 domain_whois['org_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Last Updated On':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Creation Date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Expiration Date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def tz_manage(data, domain_whois):
#     """
#     tz 提取函数
#     """
#
#     pattern = re.compile(r'(domain:(.*\n)+?contact:)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     person_id = ''
#     if match:
#         infos = match[0][0].split('\n')
#         for info in infos:
#             if info.find('changed') != -1:
#                 domain_whois['updated_date'] = info.split(':', 1)[1].strip()
#             elif info.find('expire') != -1:
#                 domain_whois['expiration_date'] = info.split(':', 1)[1].strip()
#             elif info.find('registered') != -1:
#                 domain_whois['creation_date'] = info.split(':', 1)[1].strip()
#             elif info.find('registrant') != -1:
#                 person_id = info.split(':', 1)[1].strip()
#
#     pattern_2 = re.compile(r'(contact:(.*\n)+?changed:)')
#     match_2 = pattern_2.findall(data)
#     match_length_2 = len(match_2)
#     j = 0
#     if match_2:
#         for j in range(match_length_2):
#             infos = match_2[j][0].split("\n")
#             if infos[0].split(":")[1].strip() == person_id:
#                 for info in infos:
#                     if info.split(":")[0].strip() == "e-mail":
#                         domain_whois["reg_email"] = info.split(":")[1].strip()
#                     elif info.split(":")[0].strip() == "phone":
#                         domain_whois["reg_phone"] = info.split(":")[1].strip()
#                     elif info.split(':')[0].strip() == 'org':
#                         domain_whois['org_name'] = info.split(':')[1].strip()
#                     elif info.split(':')[0].strip() == 'name':
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def uz_manage(data, domain_whois):
#     """
#     uz 提取函数
#     """
#     pattern = re.compile(
#             r'(Registrant:(.*\n)+?Expiration Date:.*)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     if match:
#         infos = match[0][0].split('\n')
#         for info in infos:
#             if info.find('Creation Date:') != -1:
#                 domain_whois['creation_date'] = info.split(':', 1)[1].strip()
#             elif info.find('Expiration Date:') != -1:
#                 domain_whois['expiration_date'] = info.split(':', 1)[1].strip()
#             elif info.find('Tel.') != -1:
#                 domain_whois['reg_phone'] = info.split('.')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def ve_manage(data, domain_whois):
#     """
#     ve 提取函数
#     """
#     pattern = re.compile(
#             r'(Fecha de Vencimiento:.*|Ultima Actualización:.*|Fecha de Creación:.*|Titular:(.*\n)+?.*Nombre de Dominio:)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('Fecha de Vencimiento:') != -1:
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Ultima Actualización:') != -1:
#                 domain_whois['updated_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Fecha de Creación:') != -1:
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Titular:') != -1:
#                 infos = match[i][0].split('\n')
#                 domain_whois['reg_name'] = infos[1].strip().split('\t\t')[0].strip()
#                 if infos[1].strip().split('\t\t')[1].strip().find('@') != -1:
#                     domain_whois['reg_email'] = infos[1].strip().split('\t\t')[1].strip()
#                 if infos[len(infos) - 3].find('(FAX)') != -1:
#                     domain_whois['reg_phone'] = infos[len(infos) - 3].split('(FAX)')[0].strip()
#                 elif not infos[len(infos) - 3].isalpha():
#                     domain_whois['reg_phone'] = infos[len(infos) - 3].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def co_za_manage(data, domain_whois):
#     """
#     co.za 提取函数
#     """
#
#     pattern = re.compile(r'(Registrant:(.*\n)+?\n|Relevant Dates:(.*\n)+?\n)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('Registrant:') != -1:
#                 infos = match[i][0].split('\n')
#                 domain_whois['reg_name'] = infos[1].strip()
#                 for info in infos:
#                     if info.find('Email:') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#                     elif info.find('Tel:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#             if match[i][0].find('Relevant Dates:') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('Registration Date:') != -1:
#                         domain_whois['creation_date'] = info.split(':', 1)[1].strip()
#                     elif info.find('Renewal Date:') != -1:
#                         domain_whois['expiration_date'] = info.split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def dz_manage(data, domain_whois):
#     """
#     dz 提取函数
#     """
#
#     pattern = re.compile(
#             r'(Description#.*|Date de creation#.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].find('Description#') != -1:
#                 domain_whois['reg_name'] = match[i].split('#')[1].strip('. ')
#             elif match[i].find('Date de creation#') != -1:
#                 domain_whois['creation_date'] = match[i].split('#')[1].strip('. ')
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def xn__j1amh_manage(data, domain_whois):
#     """
#     укр 提取函数
#     """
#     pattern = re.compile(
#             r'(Registrant Phone:.*|Registrant Name \(Organization\):.*|Registrant Organization:.*|Registrant Email:.*|Updated Date:.*|Creation Date:.*|Expiration Date:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registrant Phone':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Name (Organization)':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Email':
#                 domain_whois['reg_email'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Phone':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Updated Date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Creation Date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Expiration Date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_do_reg_manage(data, domain_whois):
#     pattern = re.compile(
#             r'(\[Creation Date\].*|\[Expiration Date\].*|\[Last Update\].*|\[Registrant\](.*\n)+?\n)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('[Creation Date]') != -1:
#                 domain_whois['creation_date'] = match[i][0].split(']')[1].strip()
#             elif match[i][0].find('[Expiration Date]') != -1:
#                 domain_whois['expiration_date'] = match[i][0].split(']')[1].strip()
#             elif match[i][0].find('[Last Update]') != -1:
#                 domain_whois['updated_date'] = match[i][0].split(']')[1].strip()
#             elif match[i][0].find('[Registrant]') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('Name:') != -1:
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#                     elif info.find('Organization:') != -1:
#                         domain_whois['org_name'] = info.split(':')[1].strip()
#                     elif info.find('E-mail:') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#                     elif info.find('Phone-Number:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_enetica_manage(data, domain_whois):
#     pattern = re.compile(
#             r'(Record last updated on.*|Record created on.*|Record expires on.*|Registrant Details:(.*\n)+?\n)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('Record created on') != -1:
#                 domain_whois['creation_date'] = match[i][0].split('on')[1].strip()
#             elif match[i][0].find('Record expires on') != -1:
#                 domain_whois['expiration_date'] = match[i][0].split('on')[1].strip()
#             elif match[i][0].find('Record last updated on') != -1:
#                 domain_whois['updated_date'] = match[i][0].split('on')[1].strip()
#             elif match[i][0].find('Registrant Details:') != -1:
#                 infos = match[i][0].split('\n')
#                 if len(infos[1].strip().split('  ')) == 2 and infos[1].strip().split('  ')[1].find('@') != -1:
#                     domain_whois['reg_name'] = infos[1].strip().split('  ')[0].strip()
#                     domain_whois['reg_email'] = infos[1].strip().split('  ')[1].strip()
#                 else:
#                     domain_whois['reg_name'] = infos[1].strip()
#                 if infos[len(infos) - 3].find('+') != -1 and infos[len(infos) - 3].strip().replace('+', '').replace('.',
#                                                                                                                     '').isdigit() == True:
#                     domain_whois['reg_phone'] = infos[len(infos) - 3].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_aitdomains_manage(data, domain_whois):
#     pattern = re.compile(
#             r'(Record last updated on.*|Record Created on.*|Expire on.*|Registrant Contact(.*\n)+?Administrative Contact)')
#
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('Record Created on') != -1:
#                 domain_whois['creation_date'] = match[i][0].split('on')[1].strip('.').strip()
#             elif match[i][0].find('Expire on') != -1:
#                 domain_whois['expiration_date'] = match[i][0].split('on')[1].strip('.').strip()
#             elif match[i][0].find('Record last updated on') != -1:
#                 domain_whois['updated_date'] = match[i][0].split('on')[1].strip('.').strip()
#             elif match[i][0].find('Registrant Contact') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('Organization Name:') != -1:
#                         domain_whois['org_name'] = info.split(':')[1].strip()
#                     elif info.split(':')[0].strip() == 'Name':
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#                     elif info.find('Email Address:') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#                     elif info.find('Phone Number:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_ibi_manage(data, domain_whois):
#     pattern = re.compile(
#             r'(Registrant :(.*\n)+?\n.*|Record created on.*|Record last updated on.*|Record expires on.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('Registrant :') != -1:
#                 infos = match[i][0].split('\n')
#                 line = infos[1].strip()
#                 if len(line.split('\t')) == 2:
#                     if line.split('\t')[1].find('@') != -1:
#                         domain_whois['reg_email'] = line.split('\t')[1].strip()
#                         domain_whois['reg_name'] = line.split('\t')[0].strip()
#                 else:
#                     domain_whois['reg_name'] = line.strip()
#                 line_phone = infos[len(infos) - 3].strip()
#                 if line_phone.find('+') != -1 and line_phone.replace('+', '').replace('.', '').isdigit() == True:
#                     domain_whois['reg_phone'] = line_phone
#             elif match[i][0].find('Record last updated on') != -1:
#                 domain_whois['updated_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Record created on') != -1:
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Record expires on') != -1:
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_networking4all_manage(data, domain_whois):
#     pattern = re.compile(
#         r'(Registrant:(.*\n)+?Administrative contact:|Updated date.*:.*|Created date.*:.*|Expiration date.*:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('Updated date..') != -1:
#                 domain_whois['updated_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Created date..') != -1:
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Expiration date..') != -1:
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Registrant:') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('Name....') != -1:
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#                     elif info.find('E-mail....') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#                     elif info.find('Phone....') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_dotroll_manage(data, domain_whois):
#     pattern = re.compile(r'(Registrant:(.*\n)+?\n|Last updated:.*|Record created:.*|Domain Expires:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('Last updated:') != -1:
#                 domain_whois['updated_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Record created:') != -1:
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Domain Expires:') != -1:
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Registrant:') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('Name:') != -1:
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#                     elif info.find('Email:') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#                     elif info.find('Phone:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#                     elif info.find('Company:') != -1:
#                         domain_whois['org_name'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_ownidentity_manage(data, domain_whois):
#     pattern = re.compile(r'(\[registrant\](.*\n)+?\[admin_c\]|Registration Date:.*|Expiration Date:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('Registration Date:') != -1:
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Expiration Date:') != -1:
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('[registrant]') != -1:
#                 infos = match[i][0].split('\n')
#                 phone_number = ''
#                 phone_prefix = ''
#                 for info in infos:
#                     if info.find('Name:') != -1:
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#                     elif info.find('Email:') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#                     elif info.find('Phone Number:') != -1:
#                         phone_number = info.split(':')[1].strip()
#                     elif info.find('Phone Prefix:') != -1:
#                         phone_prefix = info.split(':')[1].strip()
#                     elif info.find('Organization:') != -1:
#                         domain_whois['org_name'] = info.split(':')[1].strip()
#                 if phone_number:
#                     if phone_prefix:
#                         domain_whois['reg_phone'] = phone_prefix + '.' + phone_number
#                     else:
#                         domain_whois['reg_phone'] = phone_number
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_51web_manage(data, domain_whois):
#     pattern = re.compile(r'(Date Registered:.*|Expiration Date:.*|Registrant:(.*\n)+?\n)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('Date Registered:') != -1:
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Expiration Date:') != -1:
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Registrant:') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('Name') != -1:
#                         domain_whois['reg_name'] = info.split('Name')[1].strip()
#                     elif info.find('Email') != -1:
#                         domain_whois['reg_email'] = info.split('Email')[1].strip()
#                     elif info.find('Telephone') != -1:
#                         domain_whois['reg_phone'] = info.split('Telephone')[1].strip()
#                     elif info.find('Organization') != -1:
#                         domain_whois['org_name'] = info.split('Organization')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_serveisweb_manage(data, domain_whois):
#     pattern = re.compile(r'(domain_dateregistered:.*|domain_datebilleduntil:.*\
# |registrant_contact_organization:.*|registrant_contact_name:.*|registrant_contact_phone:.*\
# |registrant_contact_email:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'domain_dateregistered':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'domain_datebilleduntil':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'registrant_contact_name':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'registrant_contact_phone':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'registrant_contact_email':
#                 domain_whois['reg_email'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'registrant_contact_organization':
#                 domain_whois['org_name'] = match[i].split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_ownregistrar_manage(data, domain_whois):
#     pattern = re.compile(r'(Creation Date:.*|Expiration Date:.*|Registrant Contact Details:(.*\n)+?\n)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].split(':')[0].strip() == 'Creation Date':
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'Expiration Date':
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Registrant Contact Details:') != -1:
#                 infos = match[i][0].split('\n')
#                 domain_whois['reg_name'] = infos[1].strip()
#                 for info in infos:
#                     if info.find('Tel No.') != -1:
#                         domain_whois['reg_phone'] = info.split('No.')[1].strip()
#                     elif info.find('Email Address:') != -1:
#                         domain_whois['reg_email'] = info.split('No.')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_ksdom_manage(data, domain_whois):
#     pattern = re.compile(r'(Updated Date:.*|Creation Date:.*|Expiration Date:.*|Registant :(.*\n)+?Fax)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].split(':')[0].strip() == 'Creation Date':
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'Expiration Date':
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'Updated Date':
#                 domain_whois['updated_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Registant :') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('Registant :') != -1:
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#                     elif info.find('Phone :') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#                     elif info.find('Email :') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_nayana_manage(data, domain_whois):
#     pattern = re.compile(r'(Updated Date:.*|Registered Date:.*|Expiration Date:.*|Registrant:.*|Registrant Email:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registered Date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Expiration Date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Updated Date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Email':
#                 domain_whois['reg_email'] = match[i].split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_allglobalnames_manage(data, domain_whois):
#     pattern = re.compile(r'(Owner Name:.*|Owner Phone:.*|Owner email:.*|registration_date:.*|expiration_date:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'registration_date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'expiration_date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Owner Name':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Owner email':
#                 domain_whois['reg_email'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0] == 'Owner Phone':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_humeia_manage(data, domain_whois):
#     pattern = re.compile(
#         r'(LASTMODIFIEDDATE:.*|REGISTERDATE:.*|EXPIREDATE:.*|REGISTRANTFIRSTNAME:.*\nREGISTRANTLASTNAME:.*|REGISTRANTNAME:.*|REGISTRANTORGANIZATION:.*|REGISTRANTPHONE:.*|REGISTRANTEMAIL:.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'REGISTERDATE':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'EXPIREDATE':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'LASTMODIFIEDDATE':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].find('REGISTRANTFIRSTNAME') != -1:
#                 first_name = match[i].split('\n')[0].split(':')[1]
#                 last_name = match[i].split('\n')[1].split(':')[1]
#                 domain_whois['reg_name'] = first_name + ' ' + last_name
#             elif match[i].split(':')[0].strip() == 'REGISTRANTEMAIL':
#                 domain_whois['reg_email'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0] == 'REGISTRANTPHONE':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'REGISTRANTNAME':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'REGISTRANTORGANIZATION':
#                 domain_whois['org_name'] = match[i].split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_arcticnames_manage(data, domain_whois):
#     pattern = re.compile(r'(Expiry Date:.*|Update Date:.*|Create Date:.*|Registrant:(.*\n)+?\n)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].split(':')[0].strip() == 'Expiry Date':
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'Update Date':
#                 domain_whois['updated_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'Create Date':
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Registrant:') != -1:
#                 infos = match[i][0].split('\n')
#                 domain_whois['reg_name'] = infos[1].strip()
#                 for info in infos:
#                     if info.find('Voice:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#                     elif info.find('EMail:') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_domreg_manage(data, domain_whois):
#     pattern = re.compile(r'(Expiration:.*|Created:.*|Registrant:(.*\n)+?\n)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     if match:
#         for i in range(match_length):
#             if match[i][0].split(':')[0].strip() == 'Expiration':
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'Created':
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Registrant') != -1:
#                 infos = match[i][0].split('\n')
#                 domain_whois['reg_name'] = infos[1].strip()
#                 for info in infos:
#                     if info.replace('+', '').replace('.', '').isdigit():
#                         domain_whois['reg_phone'] = info.strip()
#                     elif info.find('@') != -1:
#                         domain_whois['reg_email'] = info.strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_nordreg_manage(data, domain_whois):
#     pattern = re.compile(r'(Expire:.*|Created:.*|Type: OWNER(.*\n)+?-------------)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     if match:
#         for i in range(match_length):
#             if match[i][0].split(':')[0].strip() == 'Expire':
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'Created':
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Type: OWNER') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('Company:') != -1:
#                         domain_whois['org_name'] = info.split(':')[1].strip()
#                     elif info.find('Name:') != -1:
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#                     elif info.find('Phone:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#                     elif info.find('E-mail:') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_chinanet_manage(data, domain_whois):
#     pattern = re.compile(r'(Expiration Date:.*|Creation Date:.*|Registrant Contact:(.*\n)+?Administrative)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     if match:
#         for i in range(match_length):
#             if match[i][0].split(':')[0].strip() == 'Expiration Date':
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'Creation Date':
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Registrant Contact') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('@') != -1:
#                         email_temps = info.split(' ')
#                         for email in email_temps:
#                             if email.find('@') != -1:
#                                 domain_whois['reg_email'] = email.strip()
#                                 domain_whois['reg_name'] = info.replace(email, '').strip()
#
#                     elif info.find('telephone:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_afriregister_manage(data, domain_whois):
#     pattern = re.compile(r'(domain:(.*\n)+?\[|holder\](.*\n)+?\[)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('domain:') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('changed:') != -1:
#                         domain_whois['updated_date'] = info.split(':', 1)[1].strip()
#                     elif info.find('registered:') != -1:
#                         domain_whois['creation_date'] = info.split(':', 1)[1].strip()
#                     elif info.find('expires:') != -1:
#                         domain_whois['expiration_date'] = info.split(':', 1)[1].strip()
#
#             elif match[i][0].find('holder]') != -1:
#                 infos = match[i][0].split('\n')
#                 name_type = ''
#                 for info in infos:
#                     if info.find('type:') != -1:
#                         name_type = info.split(':')[1].strip()
#                     elif info.find('name:') != -1:
#                         if name_type == 'ORGANISATION':
#                             domain_whois['org_name'] = info.split(':')[1].strip()
#                         else:
#                             domain_whois['reg_name'] = info.split(':')[1].strip()
#                     elif info.find('phone:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#                     elif info.find('email:') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_oiinternet_manage(data, domain_whois):
#     pattern = re.compile(
#         r'(changed.*|registered_date.*|registerexpire_date.*|Registrant Contact Information(.*\n)+?\n)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].split(':')[0].strip() == 'changed':
#                 domain_whois['updated_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'registered_date':
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'registerexpire_date':
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Registrant Contact Information') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.split(':')[0].strip() == 'name':
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#                     elif info.split(':')[0].strip() == 'phone':
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#                     elif info.split(':')[0].strip() == 'email':
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_domainprocessor_manage(data, domain_whois):
#     pattern = re.compile(r'(Creation Date:.*|Expiration Date:.*|Registrant:(.*\n)+?\n)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].split(':')[0].strip() == 'Creation Date':
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'Expiration Date':
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Registrant:') != -1:
#                 infos = match[i][0].split('\n')
#                 domain_whois['reg_name'] = infos[1].strip()
#                 for info in infos:
#                     if info.find('@') != -1:
#                         for email in info.split(' '):
#                             if email.find('@') != -1:
#                                 domain_whois['reg_email'] = email.strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_alices_registry_manage(data, domain_whois):
#     pattern = re.compile(r'(Created on:.*|Expires on:.*|Last Updated on:.*|Registrant:(.*\n)+?\n)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].split(':')[0].strip() == 'Created on':
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'Expires on':
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'Last Updated on':
#                 domain_whois['updated_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Registrant:') != -1:
#                 infos = match[i][0].split('\n')
#                 domain_whois['reg_name'] = infos[1].strip()
#                 for info in infos:
#                     if info.find('@') != -1:
#                         for email in info.split(' '):
#                             if email.find('@') != -1:
#                                 domain_whois['reg_email'] = email.strip()
#                                 domain_whois['reg_name'] = info.replace(email, '').strip()
#                     elif info.find('+') != -1 and info.replace('+', '').replace('.', '').strip().isdigit():
#                         domain_whois['reg_phone'] = info.strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_turbosite_manage(data, domain_whois):
#     pattern = re.compile(r'(Record expires on.*|Record created on.*|Database last updated.*|Registrant:(.*\n)+?\n)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].split('on')[0].strip() == 'Record created':
#                 domain_whois['creation_date'] = match[i][0].split('on')[1].strip()
#             elif match[i][0].split('on')[0].strip() == 'Record expires':
#                 domain_whois['expiration_date'] = match[i][0].split('on')[1].strip()
#             elif match[i][0].split('on')[0].strip() == 'Database last updated':
#                 domain_whois['updated_date'] = match[i][0].split('on')[1].strip()
#             elif match[i][0].find('Registrant:') != -1:
#                 infos = match[i][0].split('\n')
#                 domain_whois['reg_name'] = infos[1].strip()
#                 for info in infos:
#                     if info.find('@') != -1:
#                         for email in info.split(' '):
#                             if email.find('@') != -1:
#                                 domain_whois['reg_email'] = email.strip()
#                                 domain_whois['reg_name'] = info.replace(email, '').strip()
#                     elif info.find('+') != -1 and info.replace('+', '').replace('.', '').strip().replace(' ',
#                                                                                                          '').isdigit():
#                         domain_whois['reg_phone'] = info.strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_netdorm_manage(data, domain_whois):
#     pattern = re.compile(r'(Registration Date:.*|Expiration Date:.*|Registrant(.*\n)+?Administrative Contacts)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].split(':')[0].strip() == 'Registration Date':
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].split(':')[0].strip() == 'Expiration Date':
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Registrant') != -1:
#                 infos = match[i][0].split('\n')
#                 domain_whois['reg_name'] = infos[1].strip()
#                 for info in infos:
#                     if info.find('@') != -1:
#                         domain_whois['reg_email'] = info.strip()
#                     elif info.find('+') != -1 and info.replace('+', '').replace('.', '').strip().isdigit():
#                         domain_whois['reg_phone'] = info.strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_sdsns_manage(data, domain_whois):
#     pattern = re.compile(
#         r'(Registrant Name.*|Registrant Phone.*|Registrant E-mail.*|Updated Date.*|Creation Date.*|Expiration Date.*)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i].split(':')[0].strip() == 'Registrant Name':
#                 domain_whois['reg_name'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant Phone':
#                 domain_whois['reg_phone'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Registrant E-mail':
#                 domain_whois['reg_email'] = match[i].split(':')[1].strip()
#             elif match[i].split(':')[0].strip() == 'Updated Date':
#                 domain_whois['updated_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Creation Date':
#                 domain_whois['creation_date'] = match[i].split(':', 1)[1].strip()
#             elif match[i].split(':')[0].strip() == 'Expiration Date':
#                 domain_whois['expiration_date'] = match[i].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_ilait_manage(data, domain_whois):
#     pattern = re.compile(r'(Registration Data.*|Expiration Date.*|\[Owner\](.*\n)+?.*Fax)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('[Owner]') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('Organization Name') != -1:
#                         domain_whois['org_name'] = info.split(':')[1].strip()
#                     elif info.find('Contact Name') != -1:
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#                     elif info.find('Phone.....') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#                     elif info.find('Email.....') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#             elif match[i][0].find('Registration Data') != -1:
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Expiration Date') != -1:
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_badger_manage(data, domain_whois):
#     pattern = re.compile(r'(Created on:.*|Expires on:.*|Updated on:.*|Registrant:(.*\n)+?\n)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('Registrant:') != -1:
#                 infos = match[i][0].split('\n')
#                 domain_whois['reg_name'] = infos[1].strip()
#                 for info in infos:
#                     if info.find('Phone') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#                     elif info.find('Email') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#             elif match[i][0].find('Created on:') != -1:
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Expires on:') != -1:
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Updated on:') != -1:
#                 domain_whois['updated_date'] = match[i][0].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_binero_manage(data, domain_whois):
#     pattern = re.compile(r'(Created\.\.\..*|Expires\.\.\..*|Modified\.\.\..*|Owner-c:(.*\n)+?\n)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('Owner-c') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('Phone...') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#                     elif info.find('E-mail...') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#                     elif info.find('Organization.:') != -1:
#                         domain_whois['org_name'] = info.split(':')[1].strip()
#                     elif info.find('Name...') != -1:
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#             elif match[i][0].find('Created...') != -1:
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Expires...') != -1:
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Modified...') != -1:
#                 domain_whois['updated_date'] = match[i][0].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_dotearth_manage(data, domain_whois):
#     pattern = re.compile(
#         r'(Record last updated on:.*|Record expires on.*|Record created on:.*|Registrant:(.*\n)+?.*Administrative Contact:)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('Registrant:') != -1:
#                 infos = match[i][0].split('\n')
#                 domain_whois['reg_name'] = infos[1].strip()
#                 for info in infos:
#                     if info.find('@') != -1:
#                         for email in info.split(' '):
#                             if email.find('@') != -1:
#                                 domain_whois['reg_email'] = email.strip()
#                                 domain_whois['reg_name'] = info.replace(email, '').strip()
#             elif match[i][0].find('Record created on:') != -1:
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Record expires on') != -1:
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Record last updated on:') != -1:
#                 domain_whois['updated_date'] = match[i][0].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_maprilis_manage(data, domain_whois):
#     pattern = re.compile(
#         r'(Database last updated on.*|Record expires on.*|Record created on.*|Registrant:(.*\n)+?.*Fax)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('Registrant:') != -1:
#                 infos = match[i][0].split('\n')
#                 domain_whois['reg_name'] = infos[2].strip()
#                 for info in infos:
#                     if info.find('Email:') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#                     elif info.find('Phone:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#             elif match[i][0].find('Record created on') != -1:
#                 domain_whois['creation_date'] = match[i][0].split('on')[1].strip()
#             elif match[i][0].find('Record expires on') != -1:
#                 domain_whois['expiration_date'] = match[i][0].split('on')[1].strip()
#             elif match[i][0].find('Database last updated on') != -1:
#                 domain_whois['updated_date'] = match[i][0].split('on')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_domainregistry_manage(data, domain_whois):
#     pattern = re.compile(r'(Record last updated on\.\..*|Expires on\.\.\..*|Created on\.\.\..*|Registrant:(.*\n)+?\n)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('Registrant:') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('Email:') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#                     elif info.find('Phone:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#             elif match[i][0].find('Created on..') != -1:
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Expires on..') != -1:
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Record last updated on..') != -1:
#                 domain_whois['updated_date'] = match[i][0].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_worldbizdomains_manage(data, domain_whois):
#     pattern = re.compile(
#         r'(Record last updated:.*|Record expires.*|Record created:.*|Registrant Contact:(.*\n)+?.*Administrative Contact:)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('Registrant Contact:') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('@') != -1:
#                         for email in info.split(' '):
#                             if email.find('@') != -1:
#                                 domain_whois['reg_email'] = email.strip()
#                                 domain_whois['reg_name'] = info.replace(email, '').strip()
#                     elif info.find('Phone:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#             elif match[i][0].find('Record created:') != -1:
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Record expires:') != -1:
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Record last updated:') != -1:
#                 domain_whois['updated_date'] = match[i][0].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_domainguardians_manage(data, domain_whois):
#     pattern = re.compile(r'(Updated Date:.*|Creation Date:.*|Expiration Date:.*|\[holder\](.*\n)+?\[)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('[holder]') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('name:') != -1:
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#                     elif info.find('email:') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#                     elif info.find('phone:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#             elif match[i][0].find('Creation Date:') != -1:
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Expiration Date:') != -1:
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Updated Date:') != -1:
#                 domain_whois['updated_date'] = match[i][0].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_boterosolutions_manage(data, domain_whois):
#     pattern = re.compile(r'(Creado En:.*|Ultima Actualizacion:.*|Fecha de Expiracion:.*|Registrante:(.*\n)+?Contacto)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('Registrante') != -1:
#                 infos = match[i][0].split('\n')
#                 domain_whois['reg_name'] = infos[2].strip()
#                 for info in infos:
#                     if info.find('Correo Electronico:') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#                     elif info.find('Telefono:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#             elif match[i][0].find('Creado En:') != -1:
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Fecha de Expiracion:') != -1:
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('Ultima Actualizacion:') != -1:
#                 domain_whois['updated_date'] = match[i][0].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def sec_experianinteractive_manage(data, domain_whois):
#     pattern = re.compile(r'(registered:.*|expires:.*|changed:.*|\[registrant\](.*\n)+?\[)')
#     match = pattern.findall(data)
#     match_length = len(match)
#     i = 0
#     if match:
#         for i in range(match_length):
#             if match[i][0].find('[registrant]') != -1:
#                 infos = match[i][0].split('\n')
#                 for info in infos:
#                     if info.find('email:') != -1:
#                         domain_whois['reg_email'] = info.split(':')[1].strip()
#                     elif info.find('phone:') != -1:
#                         domain_whois['reg_phone'] = info.split(':')[1].strip()
#                     elif info.find('name:') != -1:
#                         domain_whois['reg_name'] = info.split(':')[1].strip()
#                     elif info.find('company:') != -1:
#                         domain_whois['org_name'] = info.split(':')[1].strip()
#             elif match[i][0].find('registered:') != -1:
#                 domain_whois['creation_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('expires:') != -1:
#                 domain_whois['expiration_date'] = match[i][0].split(':', 1)[1].strip()
#             elif match[i][0].find('changed:') != -1:
#                 domain_whois['updated_date'] = match[i][0].split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def ch_manage(data, domain_whois):
#     pattern = re.compile(r'(Holder of domain name:\n.*|First registration date:\n.*)')
#     match_list = pattern.findall(data)
#
#     for match in match_list:
#         if match.find('Holder of domain name') != -1:
#             domain_whois['reg_name'] = match.split('\n')[1].strip()
#         elif match.find('First registration date:') != -1:
#             domain_whois['creation_date'] = match.split('\n')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def hu_manage(data, domain_whois):
#     pattern = re.compile(r'(record created:.*)')
#     match_list = pattern.findall(data)
#
#     for match in match_list:
#         if match.find('record created:') != -1:
#             domain_whois['creation_date'] = match.split(':', 1)[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def ie_manage(data, domain_whois):
#     pattern = re.compile(r'(registration:.*|renewal:.*|descr:(.*\n)+?admin-c:)')
#     match_list = pattern.findall(data)
#
#     for match in match_list:
#         if match[0].find('registration:') != -1:
#             domain_whois['creation_date'] = match[0].split(':', 1)[1].strip()
#         elif match[0].find('renewal:') != -1:
#             domain_whois['updated_date'] = match[0].split(':', 1)[1].strip()
#         elif match[0].find('descr') != -1:
#             domain_whois['reg_name'] = match[0].split('\n')[0].split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def il_manage(data, domain_whois):
#     data_temp = data[data.find('query:'): data.find('person:')]
#
#     # print data_temp
#     pattern = re.compile(r'(validity:.*|changed:(.*\n)+?\n|(descr:.*\n)+?|phone:.*|e-mail:.*)')
#     match_list = pattern.findall(data_temp)
#
#     for match in match_list:
#         if match[0].find('validity:') != -1:
#             domain_whois['expiration_date'] = match[0].split(':', 1)[1].strip()
#         elif match[0].find('changed:') != -1:
#             date_info = match[0].split('\n')[-3].split(':')[1].strip().split(' ')
#             for date in date_info:
#                 if date.isalnum():
#                     domain_whois['updated_date'] = date
#         elif match[0].find('descr') != -1:
#             domain_whois['reg_name'] = match[0].split('\n')[0].split(':')[1].strip()
#         elif match[0].find('phone:') != -1:
#             domain_whois['reg_phone'] = match[0].split(':')[1].strip()
#         elif match[0].find('e-mail:') != -1:
#             domain_whois['reg_email'] = match[0].split(':')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# def kg_manage(data, domain_whois):
#     pattern = re.compile(
#             r'(Record last updated on.*|Record created:.*|Record expires on.*)')
#     match_list = pattern.findall(data)
#
#     for match in match_list:
#         if match.find('Record created:') != -1:
#             domain_whois['creation_date'] = match.split(':', 1)[1].strip()
#         elif match.find('Record expires on') != -1:
#             domain_whois['expiration_date'] = match.split('on')[1].strip()
#         elif match.find('Record last updated on') != -1:
#             domain_whois['updated_date'] = match.split('on')[1].strip()
#
#     domain_whois['details'] = str(data)
#     return domain_whois
#
#
# if __name__ == '__main__':
#     get_result("123", "123", "123", "123")

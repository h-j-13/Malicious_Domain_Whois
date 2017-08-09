# /usr/bin/python
# encoding:utf8

import re
from static import Static

def com_manage(data, domain_whois):
    """存在二级服务器的 提取函数"""
    if domain_whois['sec_whois_server'] != '':
        sec_func_name = Static.func_name.get_func_name(domain_whois['sec_whois_server'])
        if sec_func_name != None: # 存在专用的二级服务器处理函数
            try:
                domain_whois = eval('sec_func_name(data, domain_whois)')
            except Exception, e:
                Static.logger.error('domain: ' + domain_whois['domain'] + ' info_deal>error_info: ' + str(e))
    else:
        domain_whois = general_manage(data, domain_whois)
    return domain_whois


def general_manage(data, domain_whois):
    sign_not_exist_list = ['No match for', 'Available\nDomain', 'The queried object does not exist:', \
           'Requested Domain cannot be found', 'The queried object does not exist: Domain name', \
           'No Data Found', 'Domain Status: No Object Found', 'Domain not found.',
           'no matching objects found', \
           'No matching record.', 'No match', '\" is available for registration', '\"  not found', \
           'This domain name has not been registered.', 'NOT FOUND', 'Status: Not Registered', \
           'The queried object does not exists', 'Not found:', 'Object does not exists'
           ]
    for sign_not_exist in sign_not_exist_list:
        if data.find(sign_not_exist) != -1:
            domain_whois['domain_status'] = 'NOTEXIST'
            return domain_whois

    status = ''
    name_server = ''

    pattern = re.compile(r'(Last updated Date ?:.*|Last Updated On ?:.*\
|Update Date ?:.*|Registrant Phone ?:.*|Registrant Name ?:.*\
|Registrant Organization ?:.*|Registrant Email ?:.*\
|Registrant Phone Number ?:.*|Updated Date ?:.*\
|Creation Date ?:.*|Expiration Date ?:.*|Expires On ?:.*\
|Creation date ?:.*|Created Date ?:.*|Registrant Organisation ?:.*\
|Registrant E-mail ?:.*|Update date ?:.*|Created On ?:.*\
|Expiration date ?:.*|Updated date ?:.*|Updated On ?:.*\
|Registrant Firstname ?:.*\nRegistrant Lastname ?:.*|Expiry Date ?:.*\
|Create Date ?:.*|Status:.*|Registrar:.*|Name Server:.*\
|Registration Date:.*|creation date:.*|Nameservers:.*)')

    for match in pattern.findall(data):

        if match.split(':')[0].strip() == 'Registrant Phone' or \
                        match.split(':')[0].strip() == 'Registrant Phone Number':
            domain_whois['reg_phone'] = match.split(':')[1].strip()

        elif match.split(':')[0].strip() == 'Registrant Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()

        elif match.find('Firstname') != -1 and match.find('Lastname') != -1:
            reg_name = match.split('\n')[0].split(':')[1].strip() + ' ' + \
                       match.split('\n')[1].split(':')[1].strip()
            domain_whois['reg_name'] = match.split(':')[1].strip()

        elif match.split(':')[0].strip() == 'Registrant Email' or \
                        match.split(':')[0].strip() == 'Registrant E-mail':
            domain_whois['reg_email'] = match.split(':')[1].strip()

        elif match.split(':')[0].strip() == 'Registrant Organization' or \
                        match.split(':')[0].strip() == 'Registrant Organisation':
            domain_whois['org_name'] = match.split(':')[1].strip()

        elif match.split(':')[0].strip() == 'Updated Date' or \
                        match.split(':')[0].strip() == 'Update Date' or \
                        match.split(':')[0].strip() == 'Last updated Date' or \
                        match.split(':')[0].strip() == 'Update date' or \
                        match.split(':')[0].strip() == 'Last Updated On' or \
                        match.split(':')[0].strip() == 'Updated date' or \
                        match.split(':')[0].strip() == 'Updated On':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()

        elif match.split(':')[0].strip() == 'Creation Date' or \
                        match.split(':')[0].strip() == 'Creation date' or \
                        match.split(':')[0].strip() == 'Created Date' or \
                        match.split(':')[0].strip() == 'Created On' or \
                        match.split(':')[0].strip() == 'Create Date' or \
                        match.split(':')[0].strip() == 'creation date'or \
                        match.find('Registration Date:') != -1:
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()

        elif match.split(':')[0].strip() == 'Expiration Date' or \
                        match.split(':')[0].strip() == 'Expiration date' or \
                        match.split(':')[0].strip() == 'Expiry Date' or \
                        match.split(':')[0].strip() == 'Expires On':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()

        elif match.find('Status:') != -1:
            status += match.split(':', 1)[1].strip().split(' ')[0].strip()
            status += ';'

        elif match.find('Registrar:') != -1:
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()

        elif match.find('Name Server:') != -1 or \
                match.find('Nameservers:') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['domain_status'] = status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois


def cn_manage(data, domain_whois):
    if data.find('No matching record.') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Domain Status:.*|Registrant:.*|Registrant Contact Email:.*\
|Registration Time:.*|Expiration Time:.*|Sponsoring Registrar:.*|Name Server:.*)')

    for match in pattern.findall(data):
        if match.find('Domain Status:') != -1:
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.find('Registrant:') != -1:
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.find('Registrant Contact Email:') != -1:
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.find('Registration Time:') != -1:
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.find('Expiration Time:') != -1:
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.find('Sponsoring Registrar:') != -1:
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.find('Name Server:') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'
    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois


def ac_manage(data, domain_whois):
    if re.search(r'(Domain .+? is available for purchase)', data) != None:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    status = ''
    name_server = ''
    pattern = re.compile(r'(Status(\s)+?:.*|Expiry(\s)+?:.*|NS.*|Owner(.*\n)+?\n)')
    for match in pattern.findall(data):
        match = match[0]
        if match.split(':')[0].strip() == 'Status':
            status += match.split(':')[1].strip()
            status += ';'
        elif match.split(':')[0].find('NS') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'
        elif match.split(':')[0].find('Expiry') != -1:
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.find('Owner') != -1:
            infos = match.split('\n')
            domain_whois['reg_name'] = infos[0].split(':')[1].strip()
            if len(infos) > 1:
                domain_whois['org_name'] = infos[1].split(':')[1].strip()

    domain_whois['domain_status'] = status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois


def ae_manage(data, domain_whois):
    if data.find('No Data Found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    pattern = re.compile(r'(Status:.*|Registrant Contact Name:.*|Registrant Contact Email:.*\
|Registrant Contact Organisation:.*|Name Server:.*)')
    status = ''
    name_server = ''
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            status += match.split(':')[1].strip()
            status += ';'
        elif match.split(':')[0].strip() == 'Registrant Contact Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Contact Email':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Contact Organisation':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['domain_status'] = status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois


def de_manage(data, domain_whois):
    if data.find('Status: free') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    status = ''
    name_server = ''

    pattern = re.compile(r'(Nserver:.*|Status:.*|Changed:.*|)')
    for match in pattern.findall(data):
        if match.find('Nserver:') != -1:
            name_server += match.split(':', 1)[1].strip()
            name_server += ';'
        elif match.find('Status:') != -1:
            status += match.split(':', 1)[1].strip()
            status += ';'
        elif match.find('Changed:') != -1:
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()

    domain_whois['domain_status'] = status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois


def ee_manage(data, domain_whois):
    if data.find('not found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(Domain:(.*\n)+?delete:)')
    for match in pattern.findall(data):
        match = match[0]
        for line in match.split('\n'):
            if line.find('status:') != -1:
                domain_status += line.split(':')[1].strip().split('(')[0]
                domain_status += ';'
            elif line.find('registered:') != -1:
                domain_whois['creation_date'] = line.split(':', 1)[1].strip()
            elif line.find('changed:') != -1:
                domain_whois['updated_date'] = line.split(':', 1)[1].strip()
            elif line.find('expire:') != -1:
                domain_whois['expiration_date'] = line.split(':', 1)[1].strip()
    pattern = re.compile(r'(Registrant:(.*\n)+?changed:)')
    for match in pattern.findall(data):
        match = match[0]
        for line in match.split('\n'):
            if line.find('name:') != -1:
                domain_whois['reg_name'] = line.split(':')[1].strip()
            elif line.find('email') != -1:
                domain_whois['reg_email'] = line.split(':')[1].strip()

    for match in re.findall(r'(Name servers:(.*\n)+?changed)', data):
        match = match[0]
        for line in match.split('\n'):
            if line.find('nserver:') != -1:
                name_server += line.split(':')[1].strip()
                name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois


def th_manage(data, domain_whois):
    if data.find('No match for') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois
    domain_status = ''
    name_server = ''
    pattern = re.compile(
            r'(Registrar:.*|Name Server:.*|Status:.*|Updated date:.*|Created date:.*|Exp date:.*|Domain Holder:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server += match.split(':')[1].strip()
            name_server += ";"
        elif match.split(':')[0].strip() == 'Updated date':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Created date':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Exp date':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Domain Holder':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip() + ';'
    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois


def ru_manage(data, domain_whois):
    if data.find('No entries found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(
            r'(person:.*|nserver:.*|e-mail:.*|state:.*|registrar:.*|created:.*|paid-till:.*|org:.*|registrar:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'state':
            domain_status += match.split(':')[1].strip()
            if domain_status.find(',') != -1:
                domain_status = ';'.join(domain_status.split(','))
        elif match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'person':
            if match.split(':')[1].strip() != 'Private Person':
                domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'created':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'paid-till':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'org':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'e-mail':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois


def nz_manage(data, domain_whois):
    if data.find('query_status: 220 Available') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(domain_dateregistered:.*|domain_datebilleduntil:.*|domain_datelastmodified:.*|registrant_contact_name:.*|ns_name.*:.*\
|domain_delegaterequested:.*|registrar_name:.*|registrar_phone:.*|registrar_email:.*|registrant_contact_phone:.*|\
registrant_contact_email:.*)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'domain_dateregistered':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'domain_datebilleduntil':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'domain_datelastmodified':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'registrant_contact_name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrant_contact_phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrant_contact_email':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrar_name':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip()[:-3] == 'ns_name':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois


def sk_manage(data, domain_whois):
    if data.find('Not found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(
            r'(Last-update.*|Valid-date.*|dns_name.*|Domain-status.*)')

    for match in pattern.findall(data):
        if match.find('Last-update') != -1:
            domain_whois['updated_date'] = re.split(r'\s{2,}', match, 1)[1].strip()
        elif match.find('Valid-date') != -1:
            domain_whois['expiration_date'] = re.split(r'\s{2,}', match, 1)[1].strip()
        elif match.find('dns_name') != -1:
            name_server += re.split(r'\s{2,}', match, 1)[1].strip() + ';'
        elif match.find('Domain-status') != -1:
            domain_status = re.split(r'\s{2,}', match, 1)[1].strip() + ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois


def sg_manage(data, domain_whois):
    if data.find('not found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    pattern = re.compile(
            r'(Registrar:.*|Creation Date:.*|Modified Date:.*|Expiration Date:.*|Domain Status:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Modified Date':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
    for match in re.findall(r'(Registrant:(.*\n)*?.*Name:.*)', data):
        for line in match[0].split('\n'):
            if line.find('Name') != -1:
                domain_whois['reg_name'] = line.split(':', 1)[1].strip()
    for match in re.findall(r'(Name Servers:(.*\n)*?.*\n\n)', data):
        for line in match[0].split('\n'):
            if len(line) > 1 and line.find('Name Servers:') == -1:
                name_server += line.strip() + ';'
    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def ro_manage(data, domain_whois):

    if data.find('No entries found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(Registered On:.*|Registrar:.*|Domain Status:.*|Nameserver:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registered On':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Nameserver':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def rs_manage(data, domain_whois):

    if data.find('Domain is not registered') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Domain status:.*|Registration date:.*|Modification date:.*|\
Expiration date:.*|Registrar:.*|Registrant:.*|DNS:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Domain status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registration date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Expiration date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Modification date':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'DNS':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def qa_manage(data, domain_whois):
    if data.find('No Data Found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Last Modified:.*|Registrar Name:.*|Status:.* |Registrant Contact Name:.*|\
Registrant Contact Email:.*|Name Server:.*)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip() + ';'
        elif match.split(':')[0].strip() == 'Registrant Contact Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrar Name:':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server += match.split(':')[1].strip()
            name_server += ";"
        elif match.split(':')[0].strip() == 'Last Modified':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Contact Email':
            domain_whois['reg_email'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def pf_manage(data, domain_whois):
    if data.find('Domain unknown') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Status :.*|Created.*|Last renewed.*|Expire.*|\
|Name server.*|Registrar Company Name :.*|Registrant Name :.*|Registrant Company Name.*)')

    for match in pattern.findall(data):

        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip().find("Created")!=-1:
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find("Last renewed") != -1:
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find("Expire") != -1:
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find("Registrar Company Name") != -1:
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find("Registrant Name") != -1:
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find("Name server") != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'
        elif match.find('Registrant Company Name') != -1:
            domain_whois['org_name'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def om_manage(data, domain_whois):
    if data.find('No Data Found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Last Modified:.*|Registrar Name.*|Status.*|Registrant Contact Name.*|\
|Registrant Contact Email.*|Name Server:.*|)')

    for match in pattern.findall(data):

        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip().find("Last Modified") != -1:
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip().find("Registrant Contact Email") != -1:
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find("Registrar Name") != -1:
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find("Registrant Contact Name") != -1:
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find("Name Server") != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def co_za_manage(data, domain_whois):
    if data.find('Available') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Registrant:\n.*|Email:.*|Tel:.*|Registrar:\n.*\
|Registration Date:.*|Renewal Date:.*|Name Servers:(\n.*)*?\n\n|Domain Status:\n.*|)')

    for match in pattern.findall(data):
        match = match[0]
        if match.find('Domain Status:') != -1:
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.find('Registrant:') != -1:
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.find('Email:') != -1:
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.find('Tel:') != -1:
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.find('Registration Date:') != -1:
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.find('Renewal Date:') != -1:
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.find('Registrar:') != -1:
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.find('Name Servers:') != -1:
            for line in match.split('\n'):
                if len(line) > 2 and line.find('Name Servers:') == -1:
                    name_server += line.strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def si_manage(data, domain_whois):
    if data.find('No entries found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(registrar:.*|nameserver:.*|registrant:.*|status:.*|created:.*|expire:.*|nameserver:.*|)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nameserver':
            name_server += match.split(':')[1].strip()
            name_server += ";"
        elif match.split(':')[0].strip() == 'registrant':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'status':
            domain_status += ';'.join(match.split(':')[1].strip().split(',')) + ';'
        elif match.split(':')[0].strip() == 'created':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'expire':
            domain_whois['expiration_date'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def uk_manage(data, domain_whois):
    if data.find('This domain name has not been registered.') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois
    name_server = ''
    domain_status = ''
    pattern = re.compile(r'(Registrant:.*\n.*|Registrar:.*\n.*|Registered on:.*\
|Expiry date:.*|Last updated:.*|Name servers:.*(\n.*)+?\n\r\n)')
    for match in pattern.findall(data):
        match = match[0]
        if match.find('Registrant:') != -1:
            for temp in match.split('\n'):
                if len(temp) > 2 and temp.find('Registrant:') == -1:
                    domain_whois['reg_name'] = temp.strip()
        elif match.find('Name servers:') != -1:
            for line in match.split('\n'):
                if len(line) > 2 and line.find('Name servers:') == -1:
                    name_server += line.strip() + ';'
        elif match.find('Registered on:') != -1:
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.find('Expiry date:') != -1:
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.find('Last updated') != -1:
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.find('Registrar:') != -1:
            for temp in match.split('\n'):
                if len(temp) > 2 and temp.find('Registrar') == -1:
                    domain_whois['sponsoring_registrar'] = temp.strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def tm_manage(data, domain_whois):
    if data.find('available for purchase') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Status :.*|Expiry :.*|NS.*?:.*|Owner Name.*:.*|Owner OrgName.*:.*)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip() + ';'
        elif match.split(':')[0].strip() == 'Expiry':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Owner Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Owner OrgName':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(' ')[0] == 'NS':
            name_server += match.split(':')[1].strip() + ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def so_manage(data, domain_whois):
    if data.find('Not found:') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Sponsoring Registrar:.*|Domain Status:.*\
|Registrant Internationalized Name:.*|Registrant Internationalized Organization:.*|Registrant Voice Number:.*\
|Registrant Email:.*|Name Server:.*|Creation Date:.*|Expiration Date:.*\
|Last Updated On:.*| )')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Sponsoring Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Internationalized Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Internationalized Organization':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Voice Number':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Registrant Email':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server += match.split(':')[1].strip() + ';'
        elif match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Last Updated On':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def tf_manage(data, domain_whois):
    if data.find('No entries found in the AFNIC Database') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois
    domain_status = ''
    name_server = ''
    for match in re.findall(r'(nserver:.*)', data):
        if match.find('nserver:') != -1:
            name_server += match.split(':')[1].strip() + ';'
    holder_count = ''
    for match2 in re.findall(r'(domain:.*(\n.*)+?\n\n)', data):
        for match in re.findall(r'(holder-c:.*|registrar:.*|Expiry Date:.*|created:.*|last-update:.*|status:.*)'
                , match2[0]):
            if match.find('holder-c:') != -1:
                holder_count = match.split(':')[1].strip()
            elif match.find('status:') != -1:
                domain_status += match.split(':')[1].strip() + ';'
            elif match.find('created:') != -1:
                domain_whois['creation_date'] = match.split(':')[1].strip()
            elif match.find('last-update:') != -1:
                domain_whois['updated_date'] = match.split(':')[1].strip()
            elif match.find('Expiry Date:') != -1:
                domain_whois['expiration_date'] = match.split(':')[1].strip()
            elif match.find('registrar') != -1:
                domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()

    for match2 in re.findall(r'(nic-hdl:(.*\n)+?source:)', data):
        sign = False
        temp_count = ''
        for line in match2[0].split('\n'):
            if line.find('nic-hdl:') != -1:
                temp_count = line.split(':')[1].strip()
                if temp_count == holder_count:
                    sign = True
        if sign is False:
            continue
        pattern = re.compile(r'(contact:.*|phone:.*|e-mail:.*)')
        for match in pattern.findall(match2[0]):
            if match.find('contact') != -1:
                domain_whois['reg_name'] = match.split(':')[1].strip()
            elif match.find('phone') != -1:
                domain_whois['reg_phone'] = match.split(':')[1].strip()
            elif match.find('e-mail') != -1:
                domain_whois['reg_email'] = match.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois


def st_manage(data, domain_whois):
    if data.find('No entries found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(created-date:.*|updated-date:.*|expiration-date:.*\
|registrant-organization:.*|registrant-name:.*|registrant-phone:.*|registrant-email:.*|nameserver:.*)')
    for match in pattern.findall(data):

        if match.split(':')[0].strip() == 'registrant-phone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrant-email':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrant-name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'created-date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'updated-date':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'expiration-date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'registrant-organization':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nameserver':
            name_server+=match.split(':')[1].strip()
            name_server+=";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def sn_manage(data, domain_whois):
    if data.find('NOT FOUND') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois
    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(Date de creation:.*|Derniere modification:.*\
|Date d.expiration:.*|Nom Registrant.*|Telephone Registrant:.*\
|Courriel Registrant.:.*|Serveur.*?:.*|Registrar.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Telephone Registrant':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Courriel Registrant.':
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Nom Registrant':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == "Date de creation":
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Derniere modification':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == "Date d'expiration":
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.find('Serveur') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ";"
    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def sh_manage(data, domain_whois):
    if data.find('available for purchase') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(Status :.*|Expiry :.*|Owner Name.*:.*|Owner OrgName.*|NS.*|>*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip() + ';'
        elif match.split(':')[0].strip() == 'Expiry':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Owner Name':
            domain_whois['reg_name'] += match.split(':')[1].strip()
        elif match.find('Owner OrgName') != -1:
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find('NS') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ";"
    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def pr_manage(data, domain_whois):
    if data.find('not registered') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois
    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(Created On:.*|Expires On:.*|DNS:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Created On':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Expires On':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'DNS':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    pattern4 = re.compile(r'(Contact:.*Registrant([\s\S]*)Contact:.*Administrative)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(Organization:.*|Name:.*|Phone:.*|E-mail:.*|)')
        data3 = "".join(tuple(match4)[0])
        for match5 in pattern5.findall(data3):
            if match5.split(':')[0].strip() == 'Organization':
                domain_whois['org_name'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip() == 'Name':
                domain_whois['reg_name'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip() == 'Phone':
                domain_whois['reg_phone'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip() == 'E-mail':
                domain_whois['reg_email'] = match5.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def ly_manage(data, domain_whois):
    if data.find('Not found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois
    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(Created:.*|Updated:.*|Expired:.*\
|Domain Status:.*|Domain servers in listed order:.*(\n.*)+?\n\n|Registrant:.*(\n.*)+?\n\n)')
    for match in pattern.findall(data):
        match = match[0]
        if match.find('Registrant:') != -1:
            infos = match.split('\n')
            domain_whois['reg_name'] = infos[1].strip()
            for line in infos:
                if line.find('Phone:') != -1:
                    domain_whois['reg_phone'] = line.split(':')[1].strip()
                elif line.find('@') != -1:
                    domain_whois['reg_email']= line.strip()
        elif match.find('Domain Status:') != -1:
            domain_status += match.split(':')[1].strip() + ';'
        elif match.split(':')[0].strip() == 'Created':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Updated':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Expired':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.find('Domain servers in listed order:') != -1:
            for line in match.split('\n'):
                if line.find('Domain servers in listed order:') == -1 and len(line) > (2):
                    name_server += line.strip() + ';'
    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def lv_manage(data, domain_whois):
    if data.find('Status: free') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois
    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(Nserver:.*|Updated:.*|Status:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Updated':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Nserver':
            name_server += match.split(':')[1].strip()
            name_server += ';'
    pattern4 = re.compile(r'([Holder].*(\n.*)+?\n\n)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(Email:.*|Phone:.*|Name:.*)')
        data3 = "".join(tuple(match4))
        for match5 in pattern5.findall(data3):
            if match5.split(':')[0].strip() == 'Email':
                domain_whois['reg_email'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip() == 'Phone':
                domain_whois['reg_phone'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip() == 'Name':
                domain_whois['reg_name'] = match5.split(':')[1].strip()
    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def kz_manage(data, domain_whois):
    if data.find('Nothing found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois
    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(server.*|Domain created:.*|Last modified :.*|Domain status :.*|Current Registar:.*\
|Using Domain Name.*(\n.*)+?\n\n)')
    for match in pattern.findall(data):
        match = match[0]
        if match.split(':')[0].strip().find('server')!=-1:
            if match.split(':')[0].strip().count('.')>2:#用于去掉一行无用的信息
                name_server += match.split(':')[1].strip()
                name_server += ';'
        elif match.split(':')[0].strip() == 'Domain created':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Last modified':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Domain status':
            domain_status += match.split(':')[1].strip().split(' ')[0].strip() + ';'
        elif match.split(':')[0].strip() == 'Current Registar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.find('Using Domain Name') != -1:
            for line in match.split('\n'):
                if line.find('Name....') != -1 and line.find('Organization Name') == -1:
                    domain_whois['reg_name'] = line.split(':')[1].strip()
                elif line.find('Organization Name') != -1:
                    domain_whois['org_name'] = line.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def im_manage(data, domain_whois):
    if data.find('not found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Expiry Date:.*|Name Server:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Expiry Date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Name Server':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    pattern2 = re.compile(r'(Domain Managers([\s\S]*)Domain Owners)')
    for match2 in pattern2.findall(data):
        pattern3 = re.compile(r'(Name:.*|)')
        data2 = "".join(tuple(match2)[0])
        for match3 in pattern3.findall(data2):
            if match3.split(':')[0].strip() == 'Name':
                domain_whois['sponsoring_registrar'] = match3.split(':')[1].strip()

    pattern4 = re.compile(r'(Domain Owners([\s\S]*)Administrative Contact)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(Name:.*|)')
        data3 = "".join(tuple(match4)[0])
        for match5 in pattern5.findall(data3):
            if match5.split(':')[0].strip() == 'Name':
                domain_whois['reg_name'] = match5.split(':')[1].strip()
    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def ws_manage(data, domain_whois):
    if data.find('No match for') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Registrar WHOIS Server:.*|Updated Date:.*|Creation Date:.*|Registrar Registration Expiration Date:.*|\
Registrar:.*|Registrar Abuse Contact Email:.*|Registrar Abuse Contact Phone:.*|Domain Status:.*|Name Server:.*)')

    for match in pattern.findall(data):
        if match.find('Domain Status:') != -1:
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.find('Name Server:') != -1:
            name_server += match.split(':')[1].strip()
            name_server += ';'
        elif match.find('Registrar WHOIS Server: ') != -1:
            domain_whois['top_whois_server'] = match.split(':')[1].strip()
        elif match.find('Updated Date:') != -1:
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.find('Creation Date:') != -1:
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.find('Expiration Date:') != -1:
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.find('Registrar:') != -1:
            domain_whois['reg_name'] = match.split(':', 1)[1].strip()
        elif match.find('Registrar Abuse Contact Email:') != -1:
            domain_whois['reg_email'] = match.split(':', 1)[1].strip()
        elif match.find('Registrar Abuse Contact Phone:') != -1:
            domain_whois['reg_phone'] = match.split(':', 1)[1].strip()
    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def au_manage(data, domain_whois):
    if data.find('No Data Found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois
    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(Status:.*|Registrant Contact Name:.*\
|Registrar Name:.*|Registrant Contact Email:.*|Name Server:.*|Last Modified:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Registrant Contact Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip().split(' ')[0].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Registrant Contact Email':
            domain_whois['reg_email'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrar Name':
            domain_whois['sponsoring_registrar'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Last Modified':
            domain_whois['updated_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip().find("Name Server")!=-1:
            name_server += match.split(':')[1].strip()
            name_server += ';'
    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def ax_manage(data, domain_whois):
    if data.find('No records matching') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois
    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(Name:.*|Organization:.*|Email address:.*|Telephone:.*|Created:.*|Name Serve.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Organization':
            domain_whois['org_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Email address':
            domain_whois['reg_email'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Created':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Telephone':
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip().find("Name Serve")!=-1:
            name_server += match.split(':')[1].strip()
            name_server += ';'
    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def ca_manage(data, domain_whois):
    if re.search(r'Domain status:.*available', data) != None:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(Domain status:.*|Registrar:.*\n.*Name:.*\
|Registrant:.*\n.*Name:.*|Creation date:.*|Expiry date:.*|Updated date:.*|Name servers:.*(\n.*)+?\n\n)')
    for match in pattern.findall(data):
        match = match[0]
        if match.split(':')[0].strip() == 'Creation date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Expiry date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Updated date':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Domain status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.find('Registrar:') != -1:
            for line in match.split('\n'):
                if line.find('Name:') != -1:
                    domain_whois['sponsoring_registrar'] = line.split(':')[1].strip()
        elif match.find('Registrant:') != -1:
            for line in match.split('\n'):
                if line.find('Name:') != -1:
                    domain_whois['reg_name'] = line.split(':')[1].strip()
        elif match.find('Name servers:') != -1:
            for line in match.split('\n'):
                if len(line) > 2 and line.find('Name servers:') == -1:
                    name_server += line.strip() + ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def dk_manage(data, domain_whois):
    if data.find('NOT FOUND') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois
    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(Status:.*|Registered:.*|Expires:.*|Hostname:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Registered':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Expires':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Hostname':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def dm_manage(data, domain_whois):
    if data.find('NOT FOUND') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois
    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(registrar:.*|status:.*|created date:.*|updated date:.*|expiration date:.*|owner-name:.*|nameserver:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'created date':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'updated date':
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'expiration date':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'owner-name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nameserver':
            name_server += match.split(':')[1].strip()
            name_server += ";"
        elif match.find('registrar:') != -1:
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def dz_manage(data, domain_whois):
    if data.find('NO OBJECT FOUND') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois
    domain_status = ''
    name_server = ''
    pattern = re.compile(
        r'(Date de creation#.*|Registrar#.*)')
    for match in pattern.findall(data):
        if match.split('#')[0].strip().find('Registrar') != -1:
            domain_whois['sponsoring_registrar'] = match.split('#')[1].strip('. ').strip()
        elif match.split('#')[0].strip().find('Date de creation') != -1:
            domain_whois['creation_date'] = match.split('#')[1].strip('. ').strip()
    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def fi_manage(data, domain_whois):
    if data.find('Domain not found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(phone:.*|status:.*|created:.*|modified:.*|expires:.*|nserver:.*)')
    for match in pattern.findall(data):
        if match.find('nserver:') != -1:
            name_server += match.split(':')[1].replace('[Ok]', '').strip() + ';'
        elif match.find('phone:') != -1:
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.find('status:') != -1:
            domain_status += match.split(':')[1].strip() + ';'
        elif match.find('created:') != -1:
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.find('modified:') != -1:
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.find('expires:') != -1:
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def gd_manage(data, domain_whois):
    if data.find('not found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(registrar:.*|status:.*|created date:.*\
|updated date:.*|expiration date:.*|nameserver:.*|owner-organization:.*|owner-name:.*|owner-phone:.*|owner-email:.*)')
    for match in pattern.findall(data):
        if match.find('nameserver:') != -1:
            name_server += match.split(':')[1].strip() + ';'
        elif match.find('owner-phone:') != -1:
            domain_whois['reg_phone'] = match.split(':')[1].strip()
        elif match.find('status:') != -1:
            domain_status += match.split(':')[1].strip() + ';'
        elif match.find('created date:') != -1:
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.find('updated date:') != -1:
            domain_whois['updated_date'] = match.split(':', 1)[1].strip()
        elif match.find('expiration date') != -1:
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.find('owner-name:') != -1:
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.find('owner-email') != -1:
            domain_whois['reg_email'] = match.split(':')[1].strip()
        elif match.find('owner-organization') != -1:
            domain_whois['org_name'] = match.split(':')[1].strip()
    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def hk_manage(data, domain_whois):
    if data.find('not been registered') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Domain Status:.*|Registrar Name:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'expire':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrar Name':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Domain Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'

    pattern2 = re.compile(r'(Name Servers Information:.*(\n.*)*?Status Information:)')
    for match2 in pattern2.findall(data):
        for line in match2[0].split('\n'):
            if len(line) > 2 and line.find('Name Servers Information:') == -1:
                name_server += line.strip() + ';'

    pattern4 = re.compile(r'(Registrant Contact Information:([\s\S]*?)\n\n\n)')
    for match4 in pattern4.findall(data):
        pattern5 = re.compile(r'(Company English Name.*|Expiry Date:.*|Domain Name Commencement Date:.*\
|Phone:.*|Email:.*)')
        for match5 in pattern5.findall(match4[0]):
            if match5.split(':')[0].strip().find('Company English Name')!=-1:
                domain_whois['org_name'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip() == 'Expiry Date':
                domain_whois['expiration_date'] = match5.split(':', 1)[1].strip()
            elif match5.split(':')[0].strip() == 'Domain Name Commencement Date':
                domain_whois['creation_date'] = match5.split(':', 1)[1].strip()
            elif match5.split(':')[0].strip() == 'Phone':
                domain_whois['reg_phone'] = match5.split(':')[1].strip()
            elif match5.split(':')[0].strip() == 'Email':
                domain_whois['reg_email'] = match5.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def ug_manage(data, domain_whois):
    if data.find('No entries found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois
    domain_status = ''
    name_server = ''
    for match in re.findall(r'(Domain:.*(\n.*)+?\n\n)', data):
        for line in match[0].split('\n'):
            if line.find('Description:') != -1:
                domain_whois['reg_name'] = line.split(':')[1].strip()
            elif line.find('Registered:') != -1:
                domain_whois['creation_date'] = line.split(':', 1)[1].strip()
            elif line.find('Expiry:') != -1:
                domain_whois['expiration_date'] = line.split(':', 1)[1].strip()
            elif line.find('Nameserver:') != -1:
                name_server += line.split(':')[1].strip() + ';'
            elif line.find('Updated:') != -1:
                domain_whois['updated_date'] = line.split(':', 1)[1].strip()
            elif line.find('Status:') != -1:
                domain_status += line.split(':')[1].strip() + ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def hr_manage(data, domain_whois):
    if data.find('NOT FOUND') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois
    domain_status = ''
    name_server = ''
    sign = True
    for match in re.findall(r'(descr:.*|expires:.*)', data):
        if match.find('descr:') != -1 and sign:
            domain_whois['reg_name'] = match.split(':')[1].strip()
            sign = False
        elif match.find('expires') != -1:
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def hu_manage(data, domain_whois):
    if data.find('No match') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois
    domain_status = ''
    name_server = ''
    for match in re.findall(r'(record created:.*)', data):
        if match.find('record created:') != -1:
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def by_manage(data, domain_whois):
    if data.find('not exists') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois
    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(Registrar:.*|Updated Date:.*|Creation Date:.*|Expiration Date:.*|Domain Name Administrator:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Domain Name Administrator':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Updated Date':
            domain_whois['updated_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Creation Date':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':',1)[1].strip()
    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def ie_manage(data, domain_whois):
    if data.find('Not Registered') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    sign = True
    pattern = re.compile(r'(descr:.*|registration:.*|renewal:.*|nserver:.*|ren-status:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'registration':
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'renewal':
            domain_whois['expiration_date'] = match.split(':', 1)[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server += match.split(':')[1].strip()
            name_server += ';'
        elif match.find('descr:') != -1 and sign:
            domain_whois['reg_name'] = match.split(':')[1].strip()
            sign = False
        elif match.find('ren-status') != -1:
            domain_status += match.split(':')[1].strip() + ';'

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def il_manage(data, domain_whois):
    if data.find('No data was found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    sign = True
    for match in re.findall(r'(descr:.*(\n.*)+?\n\n)', data):
        match = match[0]
        for line in match.split('\n'):
            if sign and line.find('descr:') != -1:
                domain_whois['reg_name'] = line.split(':')[1].strip()
                sign = False
            elif line.find('nserver:') != -1:
                name_server += line.split(':')[1].strip() + ';'
            elif line.find('status:') != -1:
                domain_status += line.split(':')[1].strip() + ';'
            elif line.find('validity:') != -1:
                domain_whois['expiration_date'] = line.split(':',1)[1].strip()
            elif line.find('phone:') != -1:
                domain_whois['reg_phone'] = line.split(':')[1].strip()
            elif line.find('e-mail:') != -1:
                domain_whois['reg_email'] = line.split(':')[1].strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def lt_manage(data, domain_whois):
    if re.search(r'Status:.*available', data) != None:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(Status:.*|Registered:.*|Registrar:.*|Nameserver:.*|)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'Registered':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Nameserver':
            name_server += match.split(':')[1].strip()
            name_server += ";"
        elif match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def lu_manage(data, domain_whois):
    if data.find('No such domain') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(domaintype:.*|nserver:.*|registered:.*|org-name:.*|registrar-name:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'domaintype':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'registered':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server += match.split(':')[1].strip()
            name_server += ";"
        elif match.split(':')[0].strip() == 'registrar-name':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'org-name':
            domain_whois['org_name'] = match.split(':')[1].strip()
    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')

    return domain_whois

def mx_manage(data, domain_whois):
    if data.find('Object_Not_Found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(Created On:.*|Expiration Date:.*|Last Updated On:.*|Registrar:.*|DNS:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'Registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Created On':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Expiration Date':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'Last Updated On':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'DNS':
            name_server += match.split(':')[1].strip()
            name_server += ';'

    for match in re.findall(r'(Registrant:.*\n.*Name:.*)', data):
        for line in match.split('\n'):
            if line.find('Name:') != -1:
                domain_whois['reg_name'] = line.split(':')[1].strip()
    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(':')
    return domain_whois

def nc_manage(data, domain_whois):
    if data.find('No entries found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois
    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(Created on.*:.*|Expires on.*:.*|Last updated on.*:.*\
|Domain server.*|Registrant name.*:.*)')
    for match in pattern.findall(data):
        if match.split(':')[0].strip().find('Domain server')!=-1:
            name_server += match.split(':')[1].strip()
            name_server += ';'
        elif match.split(':')[0].strip() == 'Created on':
            domain_whois['creation_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Expires on':
            domain_whois['expiration_date'] = match.split(':',1)[1].strip()
        elif match.split(':')[0].strip() == 'Registrant name':
            domain_whois['reg_name'] = match.split(':')[1].strip()
    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois


def nu_manage(data, domain_whois):
    if data.find('not found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois
    domain_status = ''
    name_server = ''

    pattern = re.compile(r'(status:.*|holder:.*|created:.*|modified:.*|expires:.*\
|nserver:.*|registrar:.*)')

    for match in pattern.findall(data):
        if match.split(':')[0].strip() == 'status':
            domain_status += match.split(':')[1].strip()
            domain_status += ';'
        elif match.split(':')[0].strip() == 'created':
            domain_whois['creation_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'expires':
            domain_whois['expiration_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'modified':
            domain_whois['updated_date'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'holder':
            domain_whois['reg_name'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'registrar':
            domain_whois['sponsoring_registrar'] = match.split(':')[1].strip()
        elif match.split(':')[0].strip() == 'nserver':
            name_server += match.split(':')[1].strip()
            name_server += ";"

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

def sm_manage(data, domain_whois):
    if data.find('No entries found') != -1:
        domain_whois['domain_status'] = 'NOTEXIST'
        return domain_whois

    domain_status = ''
    name_server = ''
    pattern = re.compile(r'(Owner:.*(\n.*)+?\n\n|Registration date:.*|Status:.*|DNS Servers:.*(\n.*)\n\n)')
    for match in pattern.findall(data):
        match =  match[0]
        if match.find('Owner:') != -1:
            domain_whois['reg_name'] = match.split('\n')[2].strip()
            for line in match.split('\n'):
                if line.find('Phone:') != -1:
                    domain_whois['reg_phone'] = line.split(':')[1].strip()
                elif line.find('Email:') != -1:
                    domain_whois['reg_email'] = line.split(':')[1].strip()
        elif match.find('Registration date:') != -1:
            domain_whois['creation_date'] = match.split(':', 1)[1].strip()
        elif match.find('Status:') != -1:
            domain_status += match.split(':')[1].strip()
        elif match.find('DNS Servers:') != -1:
            for line in match.split('\n'):
                if len(line) > 2 and line.find('DNS Servers:') == -1:
                    name_server += line.strip()

    domain_whois['domain_status'] = domain_status.strip(';')
    domain_whois['name_server'] = name_server.strip(';')
    return domain_whois

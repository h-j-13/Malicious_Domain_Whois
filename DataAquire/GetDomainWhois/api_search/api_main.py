# /usr/bin/python
# encoding:utf-8

import json

from flask import Flask, request

from static import Static
from domain_analyse import DomainAnalyse
from update_record import update_not_deal_method, update_record, update_not_tld_record
from get_whois import get_whois

app = Flask(__name__)

@app.route('/WhoisSearch', methods = ['GET'])
def whois_search():
    try:
        domain = request.args.get('domain')
        exist = True if request.args.get('exist') == '1' else False
        return json.dumps(deal_api_search(domain, exist))
    except Flask.error_handlers:
        return json.dumps({'error': 'format error'})
    except Exception:
        return json.dumps({'error': 'other error'})

def deal_api_search(domain, exist):
    an = DomainAnalyse(domain)
    domain_punycode = an.get_punycode_domain()
    tld = an.get_punycode_tld()
    whois_srv = Static.whois_addr.get_server_addr(tld)
    # 无该域名后缀记录
    if whois_srv is None:
        update_not_tld_record(domain, exist)
        return {'error': 'not tld record'}
    func_name = Static.func_name.get_func_name(whois_srv)
    if func_name is None:
        update_not_deal_method(domain, exist)
        return {'error': 'not deal methed'}

    domain_info = {'domain': domain_punycode,
                   'whois_srv': whois_srv,
                   'func_name': func_name,
                   'exist': exist
                   }
    whois_info = get_whois(domain_info)
    domain_whois = update_record(whois_info)
    if not domain_whois:
        return {'error': 'other error'}
    return domain_whois

def open_search_api():
    print Static.get_now_time(), '打开查询api 端口:', Static.WEB_SERVER_PORT
    app.run()

if __name__ == '__main__':
    Static.init()
    open_search_api()
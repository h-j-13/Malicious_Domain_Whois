import tornado.web
import tldextract
from get_data import *

class HomePage(tornado.web.RequestHandler):
    def get(self,):
        return self.render("index.html")

class MalRegistrarHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET')
        self.finish(get_malicious_sponsoring_registrar())

class MalTldHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET')

        self.finish(get_malicious_tld())

class BlackNameHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET')

        num = int(self.get_argument("value"))
        self.finish(get_black_name(num))

class BlackEmailHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET')

        num = int(self.get_argument("value"))
        self.finish(get_black_email(num))

class BlackTelHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET')

        num = int(self.get_argument("value"))
        self.finish(get_black_tel(num))

class DomainSituationHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET')

        self.finish(get_bad_domain_situation())

class IpFrequencyHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET')

        self.finish(get_ip_frequency())

class AllWhoisHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET')

        num = int(self.get_argument("value"))
        self.finish(get_malicious_domain_whois(num))

class ExAndCrHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET')

        num = int(self.get_argument("value"))
        self.finish(get_c_e_data(num))

class ExsitSituationHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET')

        self.finish(get_exist_situation())

class UpdateFrequencyHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET')

        self.finish(get_update_situation())


class RegionDomainHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET')

        num = int(self.get_argument("value"))
        self.finish(get_region_domain(num))

class CheckInfoHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET')

        input = self.get_argument("value")
        url = tldextract.extract(input)
        domain = url.domain+"."+url.suffix

        self.finish(get_check_info(hash(domain)))


class MaliciousNumHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'GET')

        self.finish(get_malicious_domain())

